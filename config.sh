#!/bin/bash

echo CodeArea.com config
echo
sudo cp CodeArea.com.conf /etc/apache2/sites-available/
sudo a2ensite CodeArea.com.conf
sudo a2enmod cgi
sudo service apache2 reload
sudo service apache2 restart
echo "Making backup of hosts file"
sudo cp /etc/hosts ~/Desktop
sudo printf "\n127.0.0.1\tCodeArea.com\n" >> /etc/hosts
echo
echo
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
sudo su
su - ${USER} &
cd $installation_folder &
./config2.sh &