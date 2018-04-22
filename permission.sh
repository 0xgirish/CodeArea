#!/bin/bash

if [[ $1 -eq 1 ]];then
	sudo chown -R $USER pyscript/ docker/
	echo completed
else
	sudo chown -R www-data pyscript
	sudo chmod -R 755 pyscript/
	sudo echo "" > pyscript/container.log
	sudo echo "" > pyscript/judge.log
	sudo chown www-data:www-data pyscript/container.log pyscript/judge.log
	sudo chown -R www-data docker/userData/
	sudo chmod -R 755 docker/userData/
fi
