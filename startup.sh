#!/bin/bash 

sudo apt-get update -y
#sudo apt-get upgrade -y
sudo apt-get install -y wget
sudo apt-get install -y python3-pip
sudo pip3 install --upgrade flask
sudo pip3 install requests

# download API service
sudo wget https://github.com/srand01/todolist4/raw/main/todolist.db
sudo wget https://raw.githubusercontent.com/srand01/todolist4/main/todolist_service.py

sudo python3 todolist_service.py
