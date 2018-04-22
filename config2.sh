#!/bin/bash

id -nG
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