# K8s Standup on Rocky 8.6

## Configure Static Route
```
Static Route: K8s
Destination Network: 10.0.10.0/24
Distance: 1
Static Route Type: Interface
Interface: Trusted LAN
```

## Set k8s Version
```
export VERSION=1.24
```

## /etc/hosts
```
10.0.0.254 node1 node1.madeof.glass
10.0.0.253 node2 node2.madeof.glass
10.0.0.252 node3 node3.madeof.glass
```

## /etc/modules-load.d/k8s.conf
```
overlay
br_netfilter
```

## /etc/sysctl.d/k8s.conf
```
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
```

## /etc/yum.repos.d/kubernetes.repo
```
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
```
sudo dnf update -y
sudo dnf install -y iproute-tc

sudo swapoff -a
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config

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

sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/CentOS_8/devel:kubic:libcontainers:stable.repo

sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/CentOS_8/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo

sudo dnf install -y crio
sudo systemctl enable --now crio

sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

## Node1: Bootstrap Cluster
```
sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --cri-socket /var/run/crio/crio.sock
kubectl taint nodes –all node-role.kubernetes.io/master-
```

## All Nodes: Set up Kube user
```
sudo useradd -m kube
sudo usermod -aG wheel kube
sudo mkdir -p /home/kube/.kube
sudo touch /home/kube/.kube/config
sudo chown -R kube:kube /home/kube/.kube
sudo chmod 600 /home/kube/.kube/config
```

## Copy /etc/kubernetes/admin.conf to /home/kube/.kube/config

## Setup Calico CNI
```
kubectl create -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
kubectl create -f https://docs.projectcalico.org/manifests/custom-resources.yaml
```

## Join Other Nodes
```
sudo kubeadm join...
```

## Configure MetalLB
```
kubectl create ns metallb
kubectl config set-context --current --namespace=metallb
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb -f k8s/infrastructure/metallb-values.yaml
```

## Configure Ceph
```

sudo ceph mgr module enable rook
```

## Configure Traefik
```
kubectl create ns traefik
kubectl config set-context --current --namespace=traefik
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik -f k8s/infrastructure/traefik-values.yaml
```
