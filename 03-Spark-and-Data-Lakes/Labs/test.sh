#!/usr/bin/env python

import boto3
from pprint import pprint

DEFAULT_REGION='eu-west-3'
YOUR_AWS_ACCESS_KEY_ID=''
YOUR_AWS_SECRET_ACCESS_KEY=''

aws_region = "eu-west-3"
aws_az1 = "eu-west-3a"
aws_az2 = "eu-west-3b"

# Define subnet and cidr
subnet_name = {
    'web1a' :'web-1a',
    'web1b' :'web-1b',
    'app1a' :'app-1a',
    'app1b' :'app-1b'
    }

vpc_cidr = '172.31.0.0/16'

public_cidr ={
    'web1a' : '172.31.1.0/24',
    'web1b' : '172.31.2.0/24',
    'app1a' : '172.31.101.0/24',
    'app1b' : '172.31.102.0/24'
    }

# Define Internet Gateway
webapp_igw = 'webapp-igw'

# Define Route Table
webapp_rt  = 'webapp-rt'

# Define security group
web_sg = 'web-sg'
app_sg ='app-sg'
db_sg  = 'db-sg'


# Utiliser resource pour avoir l'id du VPC et après utiliser le client
ec2_resource = boto3.resource('ec2',
                    aws_access_key_id=YOUR_AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=YOUR_AWS_SECRET_ACCESS_KEY,
                    region_name=DEFAULT_REGION)

ec2_client = boto3.client('ec2',
                    aws_access_key_id=YOUR_AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=YOUR_AWS_SECRET_ACCESS_KEY,
                    region_name=DEFAULT_REGION)

vpc = ec2_resource.create_vpc(CidrBlock=vpc_cidr)

# Assign a name to our VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value": "my_vpc"}])
vpc.wait_until_available()

print('VPC created successfully with VPC ID: ' + vpc.id)

# Enable GNS hostanmes and DNS Support
vpc.modify_attribute(
        EnableDnsHostnames={ 'Value': True}
    )

# Enable public dns hostname so that we can SSH into it later
#ec2_client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
#ec2_client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )

# Create public subnet
##
public_subnet = {}
for value in public_cidr.keys():
    public_subnet[value] = vpc.create_subnet(AvailabilityZone=aws_az1,CidrBlock=public_cidr[value])
    ec2_client.modify_subnet_attribute(MapPublicIpOnLaunch={'Value': True},SubnetId=public_subnet[value].id)
    print(f'Public Subnet for {value} created successfully with SUBNET ID: {public_subnet[value].id}')


# Create an internet gateway and attach to the vpc
internet_gateway = ec2_resource.create_internet_gateway()
internet_gateway.attach_to_vpc(VpcId=vpc.id)
internet_gateway.create_tags(Tags=[{"Key": "Name", "Value": "webapp-igw"}])
print(f'Internet Gateway created successfully with GATEWAY ID: {internet_gateway.id}')
print(internet_gateway)


# create a public route table and assosiate to public subnet
public_route_table = ec2_resource.create_route_table(VpcId=vpc.id)
public_route_table.associate_with_subnet(SubnetId=public_subnet.id )

# create route to Internet Gateway in public route table
public_route = ec2_client.create_route(RouteTableId=public_route_table.id, DestinationCidrBlock=source_cidr,    GatewayId=internet_gateway.id)
print('Public Route Table with ID ' + public_route_table.id + ' created successfully')
