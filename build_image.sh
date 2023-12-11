#!/bin/bash
export IP="$(ip addr show ens160  | awk '$1 == "inet" { print $2 }' | cut -d/ -f1)"
# vérifie si le dossier harbor existe
if [ ! -d "harbor" ]; then
    if [ ! -f "harbor-offline-installer-v2.10.0-rc1.tgz" ]; then
        wget https://github.com/goharbor/harbor/releases/download/v2.10.0-rc1/harbor-offline-installer-v2.10.0-rc1.tgz
        tar xvf harbor-offline-installer-v2.10.0-rc1.tgz
        # rm harbor-offline-installer-v2.10.0-rc1.tgz
    fi
    cp ./harbor.yml harbor/harbor.yml && echo 'moved'
    bash harbor/install.sh
fi
# sudo mkdir -p /var/snap/microk8s/current/args/certs.d/$IP:8081
# sudo touch /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
# echo "server = \"http://$IP:8081\" \n[host.\"http://$IP:8081\"]\ncapabilities = [\"pull\", \"resolve\"]" | tee /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
# sudo microk8s stop && sudo microk8s start
docker compose -f harbor/docker-compose.yml up -d

#docker login $IP:8081
docker build -t $IP:8081/library/webserver .
docker push $IP:8081/library/webserver:latest

microk8s kubectl delete -f k8s.yaml
microk8s kubectl apply -f k8s.yaml