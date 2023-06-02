#!/bin/sh

DEFAULT_REGION=eu-west-3
YOUR_AWS_ACCESS_KEY_ID=
YOUR_AWS_SECRET_ACCESS_KEY=


# Create an Amazon ECS CLI configuration
ecs-cli configure --cluster ec2-ecs-lab --default-launch-type EC2 --config-name ec2-ecs-lab --region $DEFAULT_REGION

# Create a profile using your access key and secret key:
ecs-cli configure profile --access-key $YOUR_AWS_ACCESS_KEY_ID --secret-key $YOUR_AWS_SECRET_ACCESS_KEY --profile-name ecs-cli-profile

# Create Your Cluster
ecs-cli up --capability-iam --size 2 --instance-type t2.medium --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

# Deploy the Compose File to a Cluster
# from the ec2-ecs-lab directory:
cd ec2-ecs-lab && ecs-cli compose up --create-log-groups --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

# View the Running Containers on the Cluster
ecs-cli ps --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

# Scale the Tasks on the Cluster
ecs-cli compose scale 2 --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

# View the Running Containers on the Cluster (should see 2)
ecs-cli ps --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

# Create an ECS Service from the Compose File
# first, stop the containers from your compose file with the ecs-cli compose down command
# so that you have an empty cluster to work with
ecs-cli compose down --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile
# then create the service
ecs-cli compose service up --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

# View the web application!
# get the IP address for your running task from the console and paste the IP address with port 80
# into a browser window


# Clean Up
# First, delete the service so that it stops the existing containers and does not try to run any more tasks
ecs-cli compose service rm --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile
# next take down your cluster, which cleans up the resources that you created
ecs-cli down --force --cluster-config ec2-ecs-lab --ecs-profile ecs-cli-profile

