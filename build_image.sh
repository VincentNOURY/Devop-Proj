#!/bin/bash

docker build -t webserver .
docker save webserver -o webserver.tar
microk8s ctr image import webserver.tar