#!/bin/bash
export IP="$(ip addr show enp0s3  | awk '$1 == "inet" { print $2 }' | cut -d/ -f1)"
docker build -t $IP:8081/library/webserver .
docker push $IP:8081/library/webserver:latest
# sudo mkdir -p /var/snap/microk8s/current/args/certs.d/$IP:8081
# sudo touch /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
# echo "server = \"http://$IP:8081\" \n[host.\"http://$IP:8081\"]\ncapabilities = [\"pull\", \"resolve\"]" | tee /var/snap/microk8s/current/args/certs.d/$IP:8081/hosts.toml
# sudo microk8s stop && sudo microk8s start
# sudo docker-compose up -f harbor/docker-compose.yml -d
microk8s kubectl delete -f k8s.yaml
microk8s kubectl apply -f k8s.yaml