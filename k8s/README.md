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
10.0.0.254 node1 node1.madeof.glass k8s-control-plane-lb
10.0.0.253 node2 node2.madeof.glass
10.0.0.252 node3 node3.madeof.glass
```

## /etc/modules-load.d/k8s.conf
```conf
overlay
br_netfilter
```

## /etc/sysctl.d/k8s.conf
```ini
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
```

## /etc/yum.repos.d/kubernetes.repo
```ini
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
```

## /etc/NetworkManager/conf.d/calico.conf
```bash
[keyfile]
unmanaged-devices=interface-name:cali*;interface-name:tunl*;interface-name:vxlan.calico;interface-name:wireguard.cali
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

#### /etc/crio/crio.conf
```toml
[crio]
[crio.api]
[crio.runtime]
selinux = false

default_capabilities = [
        "NET_RAW",
        "CHOWN",
        "DAC_OVERRIDE",
        "FSETID",
        "FOWNER",
        "SETGID",
        "SETUID",
        "SETPCAP",
        "NET_BIND_SERVICE",
        "KILL",
]
[crio.image]
[crio.network]
plugin_dirs = [
        "/opt/cni/bin",
        "/usr/libexec/cni",
]
[crio.metrics]
enable_metrics = true
metrics_port = 9537

[crio.tracing]
[crio.stats]
```

```sh
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/CentOS_8/devel:kubic:libcontainers:stable.repo

sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/CentOS_8/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo

sudo dnf install -y crio
sudo systemctl enable --now crio

export KUBE_SOCK=unix:///var/run/crio/crio.sock
```

### Containerd (alternative to CRI-O)
Containerd seems to work in a vacuum, but if you're expecting to use these boxes to run other podman/runc workloads, they might not be fully compatible with containerd. You'll need to adjust nodeRegistration in infrastructure/cluster-config.yaml.
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

export KUBE_SOCK=unix:///run/containerd/containerd.sock
```


## Install Kubernetes / Helm
```sh
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo yum versionlock kubelet kubeadm kubectl
sudo systemctl enable --now kubelet

export VERSION=
```

## Node 1: Bootstrap Cluster
```sh

sudo mkdir -p /etc/kubernetes/config
sudo cp k8s/config.mount/* /etc/kubernetes/config/
sudo sed -i "s|REPLACEME|$(head -c 32 /dev/urandom | base64)|g" /etc/kubernetes/config/secret-encryption.yaml
sudo chmod 600 /etc/kubernetes/config/secret-encryption.yaml
sudo chown root:root /etc/kubernetes/config/secret-encryption.yaml

sudo kubeadm init --config k8s/infrastructure/cluster-config.yaml --upload-certs

```

## Node 1: Security Check
```sh
stat -c %a /etc/kubernetes/manifests/kube-apiserver.yaml # 644 or better
stat -c %a /etc/kubernetes/manifests/kube-controller-manager.yaml # 644 or better
stat -c %a /etc/kubernetes/manifests/kube-scheduler.yaml # 644 or better
stat -c %a /etc/kubernetes/manifests/etcd.yaml # 644 or better
stat -c %a /etc/kubernetes/admin.conf # 644 or better
stat -c %a /etc/kubernetes/scheduler.conf # 644 or better
stat -c %a /etc/kubernetes/controller-manager.conf # 644 or better
ls -laR /etc/kubernetes/pki/*.crt # 644 or better
stat -c %a /etc/systemd/system/kubelet.service.d/10-kubeadm.conf # 644 or better
stat -c %a /etc/kubernetes/kubelet.conf # 644 or better

ls -laR /etc/kubernetes/pki/*.key # 600 or better

stat -c %a /var/lib/etcd # 700 or better
stat -c %U:%G /etc/kubernetes/manifests/kube-apiserver.yaml # root:root
stat -c %U:%G /etc/kubernetes/manifests/kube-controller-manager.yaml # root:root
stat -c %U:%G /etc/kubernetes/manifests/kube-scheduler.yaml # root:root
stat -c %U:%G /etc/kubernetes/manifests/etcd.yaml # root:root
stat -c %U:%G /etc/kubernetes/admin.conf # root:root
stat -c %U:%G /etc/kubernetes/scheduler.conf # root:root
stat -c %U:%G /etc/kubernetes/controller-manager.conf # root:root
ls -laR /etc/kubernetes/pki/ # root:root
stat -c %U:%G /etc/kubernetes/kubelet.conf # root:root
stat -c %U:%G /etc/systemd/system/kubelet.service.d/10-kubeadm.conf # root:root

stat -c %U:%G /var/lib/etcd # etcd:etcd

# TODO:
# kubeconfig
# certificate auth
# https://cloud.redhat.com/blog/guide-to-kubernetes-ingress-network-policies
# https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook
# https://media.defense.gov/2021/Aug/03/2002820425/-1/-1/0/CTR_Kubernetes_Hardening_Guidance_1.1_20220315.PDF



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
kubectl create namespace tigera-operator

helm install calico projectcalico/tigera-operator --version v3.23.1 -f k8s/infrastructure/tigera-values.yaml --namespace tigera-operator

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

## Node 1: Configure Storage (Gluster)
I'd have preferred to run Ceph, but since I'm hosting the storage cluster on the same bare metal machines as k8s, the container runtime requirements can and will conflict. You'll end up with a dead K8s or a dead Ceph sooner or later. [Gluster Installation Instructions](https://docs.rockylinux.org/guides/file_sharing/glusterfs/).
```yaml
# Configure Endpoints
apiVersion: v1
kind: Endpoints
metadata:
  name: glusterfs-cluster
  namespace: default
  labels:
    storage.k8s.io/name: glusterfs
subsets:
  - addresses:
    - ip: 10.0.0.254
      hostname: node1
    - ip: 10.0.0.253
      hostname: node2
    - ip: 10.0.0.252
      hostname: node3
    ports:
      - port: 1
---
# Configure Service
apiVersion: v1
kind: Service
metadata:
  name: glusterfs-cluster
  namespace: default
  labels:
    storage.k8s.io/name: glusterfs
spec:
  ports:
  - port: 1
```

## Node 1: Configure Traefik
```sh
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=9000/tcp
sudo firewall-cmd --reload

kubectl create ns traefik
kubectl config set-context --current --namespace=traefik
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik -f k8s/infrastructure/traefik-values.yaml

kubectl create secret generic aws-credentials --from-literal=AWS_ACCESS_KEY_ID=XXXXX --from-literal=AWS_SECRET_ACCESS_KEY=XXXXX
```
