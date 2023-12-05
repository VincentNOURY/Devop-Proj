#!/bin/bash

docker build -t webserver .
docker save webserver -o webserver.tar
microk8s ctr image import webserver.tar
microk8s kubectl delete -f k8s2.yaml
microk8s kubectl apply -f k8s2.yaml