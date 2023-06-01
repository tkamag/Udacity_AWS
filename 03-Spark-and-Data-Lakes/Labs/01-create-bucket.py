import boto3
import json
from pprint import pprint
import os
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_REGION=os.environ['DEFAULT_REGION']
AWS_SESSION_TOKEN=os.environ['AWS_SESSION_TOKEN']

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
    return json.dumps((response.get('Location')))


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
        

if __name__ == '__main__':
    # Constants
    BUCKET_NAME='tka-lake-house'
    #a=create_a_bucket(BUCKET_NAME)
    logger.info(f'Creating a Bucket...')
 
    logger.info(
        f'Bucket created with: Name: {create_a_bucket(BUCKET_NAME)}')
    logger.info(f'Bucket Created.')
    logger.info(f'Reading Default VPC ID...')
    logger.info(f'Default VPC ID: \t {return_vpc_param()}')
