# Code Area
Code Area is an competitive programming platform made using Django+Postgres and Docker. The platform is made to run in Ubuntu. An overview of the project can be found in the project_details folder.

## Requirements
Python 3+, PostreSQL, Docker, rabbitmq-server.

## Docker Installation and Docker image installation
Follow these steps for Docker installation
- cd /path/to/CodeAreaMaster/
- chmod +x config.sh config2.sh
- ./config.sh

Now docker installation has been completed
**Note: You may have to logout (or restart your machine) to allow Docker to run without sudo**

Instructions to create Docker image from Dockerfile [./backend/src/judge/Dockerfile]

- open a new terminal
- cd path/to/CodeAreaMaster/
- ./config2.sh 				**Third step may take some time**

**If above script give the error (Can't connect to docker daemon) during hello-world installation
It means docker is not allowed to run without sudo (running docker without sudo is required)
Please logout from the system (or restart your computer).
It will fix the issue.**

## rabbitmq-server installation
On Ubuntu, run the following command:
``` sudo apt install rabbitmq-server ```
To add user and password follow these commands
> sudo su
> rabbitmqctl add_user username password
> rabbitmqctl set_user_tags username administrator
> rabbitmqctl set_permissions -p / username ".*" ".*" ".*"

## Postgres Installation
On Ubuntu, run the following command:
``` sudo apt-get install postgresql postgresql-contrib ```
### Create a Database
On Ubuntu, the run the following command:
``` 
sudo su - postgres 
psql
```
Then create a database named codearea:
``` 
CREATE DATABASE codearea;
```

## Django Installation
Go to the folder backend/src/ and execute:
``` 
pip install -r requirements.txt
```
A virtual environment is recommended.
Later inside that directory, run the following command:
``` 
python manage.py makemigrations
python manage.py migrate
```
This would create the necessary tables in the postgres database. Make sure the username and password of your database is set in DATABASE variable in settings.py found in backend/src/codearea.

To create a superuser, run the following command
``` 
python manage.py createsuperuser
```

Next go to the admin panel found in host:port/admin/, then to the languages sections found in '/admin/submissions/language/' and add the following languages:
- C
- cpp14
- python2
- python3
- java
- golang

## Start the application
To start the application, simply run the server:
``` 
python manage.py runserver
```
systemd configuration
---
- add environment variables in .service file
- add path to python(anaconda3)
- set working directory according to given example
- follow these commands
	1. sudo mv codearea.service /etc/systemd/system
	2. sudo systemctl enable codearea
	3. sudo systemctl start codearea

