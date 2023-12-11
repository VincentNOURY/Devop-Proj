#!/bin/bash
docker build -t 192.168.0.78:8081/library/webserver .
docker push 192.168.0.78:8081/library/webserver:latest
# sudo mkdir -p /var/snap/microk8s/current/args/certs.d/192.168.0.78:8081
# sudo touch /var/snap/microk8s/current/args/certs.d/192.168.0.78:8081/hosts.toml
# echo "server = \"http://192.168.0.78:8081\" \n[host.\"http://192.168.0.78:8081\"]\ncapabilities = [\"pull\", \"resolve\"]" | tee /var/snap/microk8s/current/args/certs.d/192.168.0.78:8081/hosts.toml
# sudo microk8s stop && sudo microk8s start
sudo docker-compose up -f harbor/docker-compose.yml -d
microk8s kubectl delete -f k8s.yaml
microk8s kubectl apply -f k8s.yaml