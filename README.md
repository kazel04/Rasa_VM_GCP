# Rasa Deployment
Deploying Rasa Bot over Google Cloud Platform using Docker.

## Prerequisites:
- Docker
- Docker Compose


## Instructions:

### For deploying locally:

- clone this repository
- run the below command within the project directory:
>  docker-compose up --build

- Check whether the services are up and running using below command:
> docker ps -a

- test out the bot in the browser
> http://localhost

Youtube Video:

https://www.youtube.com/watch?v=9C1Km6xfdMA

### For deploying over GCP Compute Engine:
- Create the VM instance of Ubuntu over Compute Engine
- once the instance is created login to the VM using SSH
- Run the below commands and clone our Docker app:

 - > sudo apt-get update
 
#### Install Docker

- > curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add 
- > sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
- > sudo apt-get update
- >  apt-cache policy docker-ce
- > sudo apt-get install -y docker-ce
- > sudo systemctl status docker
     
#### Install [Docker-Compose](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04)

- > sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
- > ^ Copy this in readme/edit mode, otherwise there will be a formatting error

- > sudo chmod +x /usr/local/bin/docker-compose
- > docker-compose --version

#### Clone the Docker App

- > git clone [git repo here]
- > cd [git repo name]

#### Build the Docker app and run the services:

- > sudo docker-compose up --build

- Check whether the services are up and running using below command:
- > docker ps -a

- Once you see all the services up and running, open the ip address of the machine in the browser and test the bot

Youtube Video: 

https://youtu.be/qOHszxJsuGs

## Debugging Notes:
- All commands must be run in the terminal opened after SSH-ing into the GCP VM
- For NLU & stories, add your own yml to replace the md in the backend folder
- Replace the old rasa files in the backend, rasa training and model creation is from the backend folder
- When accessing the VM's external IP address for the web app demo, remember to remove the "https://" from the url 
- To update, commit new rasa files into the appropriate folders like backend, then git pull in the VM's folder of the repo and run the docker compose up command
- When creating new VM instance, allow HTTP and HTTPS traffic and allow full access to all cloud APIs
- For full reset/update, a new VM must be created as the VM still rmbs old convo paths even when deleted


