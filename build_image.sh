#!/bin/bash

docker build -t webserver .
docker push 192.168.0.78:8081/library/webserver:latest 
microk8s kubectl delete -f k8s2.yaml
microk8s kubectl apply -f k8s2.yaml