#!/bin/bash
file=harbor-offline-installer-v1.9.0.tgz
export IP="$(ip addr show ens32  | awk '$1 == "inet" { print $2 }' | cut -d/ -f1)"
# vérifie si le dossier harbor existe
if [ ! -d "harbor" ]; then
    if [ ! -f $file ]; then
        wget "https://storage.googleapis.com/harbor-releases/release-1.9.0/$file"
    fi
    sudo tar -xzvf $file
    rm $file
    sudo cp ./harbor.yml harbor/harbor.yml && echo 'moved'
    sudo bash harbor/install.sh
fi
# sudo mkdir -p /var/snap/microk8s/current/args/certs.d/$IP:8081
# sudo touch /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
# echo "server = \"http://$IP:8081\" \n[host.\"http://$IP:8081\"]\ncapabilities = [\"pull\", \"resolve\"]" | tee /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
# sudo microk8s stop && sudo microk8s start
sudo docker-compose -f harbor/docker-compose.yml up -d

sudo docker build -t $IP:8081/library/webserver .

sudo docker login $IP:8081 -u admin -p Harbor12345
sudo docker push $IP:8081/library/webserver:latest

microk8s enable metallb:192.168.1.100-192.168.1.110
microk8s kubectl delete -f k8s.yaml
microk8s kubectl apply -f k8s.yaml