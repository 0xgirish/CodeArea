#!/bin/bash

id -nG
echo 
echo "Testing docker hello-world"
docker run hello-world
echo 
echo "Testing completed"
echo
echo 'Creating image of virtual_machine (docker)'
docker build -t virtual_machine ./backend/src/judge/docker/
echo
echo Docker image virtual_machine succesfully created
echo