#!/bin/bash

echo 'Creating image of virtual_machine (docker)'
docker build -t virtual_machine ./docker/
echo
echo Docker image virtual_machine succesfully created
echo Testing image
docker run -it --rm --name tmptest -v /home/$USER/web/CodeArea/docker/userData/:/app virtual_machine:latest
echo
echo Testing completed
echo giving permissions
sudo su
chown www-data pyscript
chmod -R 755 pyscript/
echo "" > container.log
echo "" > judge.log
chown www-data:www-data pyscript/container.log pyscript/judge.log
chown -R www-data docker/userData/
chmod -R 755 docker/userData/

