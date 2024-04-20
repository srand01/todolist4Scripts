#!/bin/bash 

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y wget
sudo apt-get install -y python3-pip
sudo pip3 install --upgrade flask

# download the app code
sudo wget -P templates http://storm.cis.fordham.edu/ji/cisc5550cloud/homework3/templates/index.html
sudo wget http://storm.cis.fordham.edu/ji/cisc5550cloud/homework3/todolist.py
sudo wget http://storm.cis.fordham.edu/ji/cisc5550cloud/homework3/todolist.db

sudo python3 todolist.py
