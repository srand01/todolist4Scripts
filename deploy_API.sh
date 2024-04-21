#!/bin/bash

# Create the instance with the startup script
gcloud compute instances create todolist4 --project todolist4-4192024 --machine-type e2-micro --image-family=debian-10 --image-project debian-cloud --create-disk=size=10GB --tags http-server --zone us-east1-d --metadata-from-file=startup-script=./startup.sh

# Create the firewall rule
gcloud compute firewall-rules create rule-allow-tcp-5001 --project todolist4-4192024 --source-ranges 0.0.0.0/0 --target-tags http-server --allow tcp:5001
