# K8s Standup on Rocky 8.6

## Configure Static Route
```md
Static Route: K8s
Destination Network: 10.0.10.0/24
Distance: 1
Static Route Type: Interface
Interface: Trusted LAN
```

## Set Preferred Kubernetes Version
```sh
export VERSION=1.24
```

## /etc/hosts
```conf
10.0.0.254 node1 node1.madeof.glass
10.0.0.253 node2 node2.madeof.glass
10.0.0.252 node3 node3.madeof.glass
```

## /etc/modules-load.d/k8s.conf
```conf
overlay
br_netfilter
```

## /etc/sysctl.d/k8s.conf
```toml
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
```

## /etc/yum.repos.d/kubernetes.repo
```toml
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
```

## Setup Prerequisites
```sh
sudo dnf update -y
sudo dnf install -y iproute-tc chrony yum-utils yum-plugin-versionlock
sudo systemctl enable --now chronyd

sudo swapoff -a
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
sudo setenforce 0

sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=2379-2380/tcp
sudo firewall-cmd --permanent --add-port=10250/tcp
sudo firewall-cmd --permanent --add-port=10251/tcp
sudo firewall-cmd --permanent --add-port=10252/tcp
sudo firewall-cmd --permanent --add-port=30000-32767/tcp
sudo firewall-cmd --reload

sudo modprobe overlay
sudo modprobe br_netfilter
sudo sysctl --system
```

## Choose your Adventure: CRI-O or Containerd

### CRI-O (best option in my opinion)
CRI-O is the RHEL-oriented option, as it powers OpenShift. But you might run into permission issues when running k8s rootlessly. 
```sh
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/CentOS_8/devel:kubic:libcontainers:stable.repo

sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/CentOS_8/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo

sudo dnf install -y crio
sudo systemctl enable --now crio

export KUBE_SOCK=/var/run/crio/crio.sock
```

### Containerd (alternative to CRI-O)
Containerd seems to work in a vacuum, but if you're expecting to use these boxes to run other podman/runc workloads, they might not be fully compatible with containerd.
#### /etc/containerd/config.toml
```toml
disabled_plugins=[""]
[plugins."io.containerd.grpc.v1.cri"]
    systemd_cgroup = true

```

```sh
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# Remove podman, buildah, runc if this command fails:
sudo dnf install -y containerd.io
sudo systemctl enable --now containerd

export KUBE_SOCK=/run/containerd/containerd.sock
```


## Install Kubernetes
```sh
sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

sudo systemctl enable --now kubelet

sudo yum versionlock kubelet kubeadm kubectl

export VERSION=
```

## Node 1: Bootstrap Cluster
```sh
sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --cri-socket $KUBE_SOCK
```

## All Nodes: Set up Kube user
```sh
sudo useradd -m kube
sudo usermod -aG wheel kube
sudo mkdir -p /home/kube/.kube
```

## Node 1: Copy Kube Config / Untaint Control Plane
```sh
sudo rsync -aP /etc/kubernetes/admin.conf node1:/home/kube/.kube/config

sudo rsync -aP /etc/kubernetes/admin.conf node2:/home/kube/.kube/config

sudo rsync -aP /etc/kubernetes/admin.conf node3:/home/kube/.kube/config

sudo -u kube kubectl taint nodes --all node-role.kubernetes.io/master-
```

## All Nodes: Configure permissions
```sh
sudo chown -R kube:kube /home/kube/.kube
sudo chmod 600 /home/kube/.kube/config
```
## Reboot All Nodes
Now's a good time for a reboot. I'm not sure if it's necessary, but 'reboot early and often' is a good rule of thumb when you're about to start debugging networking configs.

## Node 1: Swap to Kube User, Untaint Control Plane
```sh
sudo -u kube -s
kubectl taint nodes --all node-role.kubernetes.io/master-
```

## Node 1: Setup Calico CNI
```sh
kubectl create -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
kubectl create -f https://docs.projectcalico.org/manifests/custom-resources.yaml
```

## All Nodes: Join Other Nodes
```sh
# On node 1...
sudo kubeadm token create  --print-join-command

# On each node...
sudo kubeadm join...
```

## Node 1: Configure MetalLB
```sh
kubectl create ns metallb
kubectl config set-context --current --namespace=metallb
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb -f k8s/infrastructure/metallb-values.yaml
```

## Node 1: Configure Storage
```sh

```

## Node 1: Configure Traefik
```sh
kubectl create ns traefik
kubectl config set-context --current --namespace=traefik
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik -f k8s/infrastructure/traefik-values.yaml
```
