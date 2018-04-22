#!/bin/bash

echo "Installing docker"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
su - ${USER}
id -nG
sudo usermod -aG docker www-data
echo "Testing docker hello-world"
docker run hello-world
echo "Testing completed"
echo
echo 'Creating image of virtual_machine (docker)'
docker build -t virtual_machine ./docker/
echo
echo Docker image virtual_machine succesfully created
echo
echo giving permissions
./permission.sh