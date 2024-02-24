
####
sudo apt update && sudo apt upgrade -y
sudo apt install rsyslog iptables -y
sudo iptables -F
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy



#### Master node installation
# curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.28.5+k3s1 INSTALL_K3S_EXEC="server --disable=traefik --flannel-backend=host-gw --tls-san=10.200.1.90 --bind-address=10.200.1.90 --advertise-address=10.200.1.90 --node-ip=10.200.1.90 --cluster-init" sh -s -

# curl -sfL https://get.k3s.io | sudo sh -

#### Install K3S v1.27.10+k3s2
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.27.10+k3s2" K3S_KUBECONFIG_MODE="644" sh -s



#### k3s configuration
/etc/rancher/k3s/k3s.yaml

#### Worker nodes installation
#### get node-token from master node
sudo cat /var/lib/rancher/k3s/server/node-token

#### Token
K103c873233b9086a8bd3f0bfd67b1efd67697a5804ec5b5dee8052bb999a5da256::server:497b4372294904ce5d149e186a95a782

# Install Worker Nodes
# curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.28.5+k3s1 K3S_URL=https://10.200.1.90:6443 \
#  K3S_TOKEN="K10985117e345c1dfdc1cd899d51c71708c8ba1337733880aeec4547cde1257f24f::server:3b811610071eafff225ed29326d5cbcb" sh -

# curl -sfL https://get.k3s.io | K3S_URL=https://10.200.1.90:6443 K3S_TOKEN=K10985117e345c1dfdc1cd899d51c71708c8ba1337733880aeec4547cde1257f24f::server:3b811610071eafff225ed29326d5cbcb sh -

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.27.10+k3s2" K3S_TOKEN="K103c873233b9086a8bd3f0bfd67b1efd67697a5804ec5b5dee8052bb999a5da256::server:497b4372294904ce5d149e186a95a782" K3S_URL="https://10.200.1.90:6443" K3S_NODE_NAME="pinode01" sh -

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.27.10+k3s2" K3S_TOKEN="K103c873233b9086a8bd3f0bfd67b1efd67697a5804ec5b5dee8052bb999a5da256::server:497b4372294904ce5d149e186a95a782" K3S_URL="https://10.200.1.90:6443" K3S_NODE_NAME="pinode02" sh -

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.27.10+k3s2" K3S_TOKEN="K103c873233b9086a8bd3f0bfd67b1efd67697a5804ec5b5dee8052bb999a5da256::server:497b4372294904ce5d149e186a95a782" K3S_URL="https://10.200.1.90:6443" K3S_NODE_NAME="pinode03" sh -

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.27.10+k3s2" K3S_TOKEN="K103c873233b9086a8bd3f0bfd67b1efd67697a5804ec5b5dee8052bb999a5da256::server:497b4372294904ce5d149e186a95a782" K3S_URL="https://10.200.1.90:6443" K3S_NODE_NAME="pinode04" sh -

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.27.10+k3s2" K3S_TOKEN="K103c873233b9086a8bd3f0bfd67b1efd67697a5804ec5b5dee8052bb999a5da256::server:497b4372294904ce5d149e186a95a782" K3S_URL="https://10.200.1.90:6443" K3S_NODE_NAME="pinode05" sh -

#### Delete k3s node
kubectl delete node <node-name>



#### Install Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh


kubectl -n kube-system delete secrets <agent-node-name>.node-password.rke2 or kubectl -n kube-system delete secrets <agent-node-name>.node-password.k3s



####
cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory


#### uninstall server
/usr/local/bin/k3s-uninstall.sh


#### uninstall workstation
/usr/local/bin/k3s-agent-uninstall.sh


#### Check Status of k3s Service
sudo cat /var/lib/rancher/k3s/server/node-token


#### Update firmware
sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update -O /usr/bin/rpi-update && sudo chmod +x /usr/bin/rpi-update


Feb 23 21:33:41 pinode01 k3s[4220]: time="2024-02-23T21:33:41-07:00" level=info msg="Waiting to retrieve agent configuration; server is not ready: Node password rejected, duplicate hostname or contents of '/etc/rancher/node/password' ma>