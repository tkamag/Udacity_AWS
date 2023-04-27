import boto3
import logging
import boto3
from botocore.exceptions import ClientError
from pprint import pprint
import json
import os
import numpy as np

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_REGION=os.environ['DEFAULT_REGION']

DWH_CLUSTER_TYPE=os.environ['DWH_CLUSTER_TYPE']
DWH_NODE_TYPE=os.environ['DWH_NODE_TYPE']
DWH_NUM_NODES=os.environ['DWH_NUM_NODES']
DWH_DB=os.environ['DWH_DB']
DWH_CLUSTER_IDENTIFIER=os.environ['DWH_CLUSTER_IDENTIFIER']
DWH_DB_USER=os.environ['DWH_DB_USER']
DWH_DB_PASSWORD=os.environ['DWH_DB_PASSWORD']
#1. Create user

def launch_redshift_cluster():
    """
    Creates an IAM user with AWS Management console access  for Redshift
    """
    redshift = boto3.client('redshift',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)
 
    try:
        response = redshift.create_cluster(        
            # add parameters for hardware                                      
            ClusterType = DWH_CLUSTER_TYPE,                 
            NodeType = DWH_NODE_TYPE,                       
            NumberOfNodes = int(DWH_NUM_NODES), 

            #Identifiers & Credentials        
            DBName= DWH_DB,                                
            Port=5439,        

            # add parameters for identifiers & credentials
            ClusterIdentifier = DWH_CLUSTER_IDENTIFIER,  
            MasterUsername= DWH_DB_USER,                    
            MasterUserPassword = DWH_DB_PASSWORD,           
            
            # add parameter for role (to allow s3 access)
            IamRoles=['arn:aws:iam::128660232396:role/myRedshiftRole'],

            #VpcSecurityGroupIds=[],
            #ClusterSubnetGroupName=,
            #ClusterSecurityGroups=[],

            AvailabilityZone=AWS_REGION,
            EnhancedVpcRouting=False,
            PubliclyAccessible=True
    )
except Exception as e:
    print(e)
