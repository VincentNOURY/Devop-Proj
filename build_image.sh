#!/bin/bash
file=harbor-offline-installer-v1.9.0.tgz
export IP="$(ip -br a | grep ens | cut -d ' ' -f 1 | xargs ip addr show | awk '$1 == "inet" { print $2 }' | cut -d/ -f1)"
export IMG_K8S="192.168.0.19:8081/library/webserver:latest"
export IP_K8S_RANGE="192.168.0.102/32"
export IP_K8S="\"192.168.0.102\""

envsubst < k8s.yaml > tmp.yaml

# vérifie si le dossier harbor existe
if [ ! -d "harbor" ]; then
    if [ ! -f $file ]; then
        wget "https://storage.googleapis.com/harbor-releases/release-1.9.0/$file"
    fi
    sudo tar -xzvf $file
    rm $file
    sed 's/192\.168\.0\.[0-9]\{1,3\}/'"$IP"'/g' -i harbor.yml
    sudo cp ./harbor.yml harbor/harbor.yml && echo 'moved'
    sudo bash harbor/install.sh
fi
if [ ! -f /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml ]; then
    sudo mkdir -p /var/snap/microk8s/current/args/certs.d/$IP:8081
    sudo touch /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
    printf "server = \"http://$IP:8081\" \n[host.\"http://$IP:8081\"]\ncapabilities = [\"pull\", \"resolve\"]" | sudo tee /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
    sudo microk8s stop && sudo microk8s start
fi
sudo docker-compose -f harbor/docker-compose.yml up -d

sudo docker build -t $IP:8081/library/webserver .

sudo docker login $IP:8081 -u admin -p Harbor12345
sudo docker push $IP:8081/library/webserver:latest

sed 's/192\.168\.0\.[0-9]\{1,3\}\:8081\/library\/webserver\:latest/'"$IP"'\:8081\/library\/webserver\:latest/g' -i tmp.yaml
microk8s enable metallb:192.168.1.100-192.168.1.110
microk8s kubectl delete -f tmp.yaml
microk8s kubectl apply -f tmp.yaml
