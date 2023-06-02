import boto3
import json
from pprint import pprint
from botocore.exceptions import ClientError
import os
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_REGION=os.environ['DEFAULT_REGION']
AWS_SESSION_TOKEN=os.environ['AWS_SESSION_TOKEN']
VPC_S3_ENDPOINT = f"com.amazonaws.{AWS_REGION}.s3"

def create_a_bucket(bucket_name):
    """
        Create an IAM role
    """
    s3_client = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
                         #, aws_session_token=AWS_SESSION_TOKEN)

    try:
        response = s3_client.create_bucket(
                        Bucket=bucket_name,
            )
    except Exception as e:
        logger.info(f'Exeption: {e}')
    #return json.dumps((response.get('Location')))
    return response.get('Location')\
                   .split('/')[-1]


def return_vpc_param():
    """
    Return parameters of default VPC.
    """
    vpc_client = boto3.client('ec2',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)
    try:
        #logger.info(f'Describing VPC...')
        response = vpc_client.describe_vpcs()
    except ClientError as e:
        logger.exception(f'Could not describe VPC : {e}')
        #pprint(vpc_client.describe_vpcs()['Vpcs'])
    for elem in vpc_client.describe_vpcs()['Vpcs']:
    #    if elem.get('InstanceTenancy') == 'default':
        return elem.get('VpcId')
    #return pprint(response)
        
def return_describe_route():
    """
    Return parameters of default VPC.
    """
    ec2_client = boto3.client('ec2',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)
    try:
        #logger.info(f'Describing VPC...')
        response = ec2_client.describe_route_tables()
    except ClientError as e:
        logger.exception(f'Could not describe route : {e}')
        #pprint(vpc_client.describe_vpcs()['Vpcs'])
    return  [elem['RouteTableId'] for elem in response.get('RouteTables')]
    #for elem in response.get('RouteTables'):
        #return elem.get('RouteTableId')
        #return elem['RouteTableId']
    #return pprint(response)
    
    
def return_vpc_endpoint(VpcId, RouteTableIds):
    """
    Return parameters of default VPC.
    """
    ec2_client = boto3.client('ec2',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)
    try:
        #logger.info(f'Describing VPC...')
        response = ec2_client.create_vpc_endpoint(VpcId=VpcId, 
                                                  RouteTableIds=RouteTableIds,
                                                  ServiceName=VPC_S3_ENDPOINT)
    except Exception as e:
        logger.info(f'Exeption: {e}')
        #pprint(vpc_client.describe_vpcs()['Vpcs'])

    return response.get('VpcEndpoint')\
                   .get('VpcEndpointId')
    
 # Use attach_role_policy to attach a managed policy to a role. To embed an inline policy in a role, use PutRolePolicy. 
 # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/attach_role_policy.html
 # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/put_role_policy.html
def create_iam_role(iam_client, GLUE_S3_ROLE_NAME):
    '''
    Creates IAM Role for Glue, to allow it to use AWS services
    '''
    
    assume_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "glue.amazonaws.com"
                    ]
                }
            }
        ]
    })
    # Create two inline policies GlueAccess  and  S3Access 
    
    s3_document = json.dumps({
		"Version":"2012-10-17",
		"Statement":{
			"Effect":"Allow",
			"Action":"s3:*",
			"Resource":"*"}
			})
  
    try:
        logger.info("1.1 - Creating a new IAM Role")
        response = iam_client.create_role(
            Path='/',
            RoleName=GLUE_S3_ROLE_NAME,
            Description=DESCRIPTION,
            AssumeRolePolicyDocument=assume_policy
            )
        
    except Exception as e:
        logger.info(f'Exeption: {e}')

    try:
        logger.info("1.2 - Attaching Policy")
        response1 = client.put_role_policy(
                    RoleName=GLUE_S3_ROLE_NAME,
                    PolicyDocument='{"Version":"2012-10-17","Statement":{"Effect":"Allow","Action":"s3:*","Resource":"*"}}',
                    PolicyName='S3AccessPolicy',
            )
    except Exception as e:
        logger.info(f'Exeption: {e}')
    #logger.info("1.3 - Get IAM role ARN")
    #roleArn = iam_client.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

    return response1

   
if __name__ == '__main__':
    # Constants
    BUCKET_NAME='tka-lake-house'
    POLICY_S3_NAME='S3Acces'
    POLICY_GLUE_NAME='GlueAccess' 
    GLUE_S3_ROLE_NAME='my-glue-service-role'
    DESCRIPTION='Grant Glue Privileges on the S3 Bucket'
    iam_client = boto3.client('iam',
                       aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
    VpcId=return_vpc_param()
    RouteTableIds=return_describe_route()

    logger.info(f'Bucket created with Name: {create_a_bucket(BUCKET_NAME)}')
    logger.info(f'Default VPC ID: {return_vpc_param()}')
    logger.info(f'Default Route ID: {return_describe_route()}')
    #logger.info(f'Vpc Endpoint: {return_vpc_endpoint(VpcId, RouteTableIds)}')
    logger.info(f'IAM role created with ID:  {create_iam_role(iam_client, GLUE_S3_ROLE_NAME)}')
 
