#!/bin/bash
sudo docker rm victim
sudo docker run --name victim --network host log4j-shell-poc
