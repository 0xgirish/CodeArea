#!/bin/bash

echo "Installing docker"
sudo apt-get update
sudo apt-get install curl
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
sudo usermod -aG docker www-data
printf "Enter installation folder:  "
read installation_folder
su - ${USER} &
cd $installation_folder &
./config2.sh &