#!/bin/bash

docker build -t 192.168.0.78:8081/library/webserver .
docker push 192.168.0.78:8081/library/webserver:latest 
microk8s kubectl delete -f k8s.yaml
microk8s kubectl apply -f k8s.yaml