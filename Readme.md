# Docker Installation and Docker image installation
Follow these steps for Docker installation
1.) cd /path/to/CodeAreaMaster/
2.) chmod +x config.sh config2.sh
3.) ./config.sh

Now docker installation has been completed
**Note: You may have to logout (or restart your machine) to allow Docker to run without sudo**

Instructions to create Docker image from Dockerfile [./backend/src/judge/Dockerfile]

1.) open a new terminal
2.) cd path/to/CodeAreaMaster/
3.) ./config2.sh 				**Third step may take some time**

**If above script give the error (Can't connect to docker daemon) during hello-world installation
It means docker is not allowed to run without sudo (running docker without sudo is required)
Please logout from the system (or restart your computer).
It will fix the issue.**
