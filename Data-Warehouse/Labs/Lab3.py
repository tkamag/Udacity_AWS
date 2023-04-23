import boto3
import logging
import json
from pprint import pprint
from botocore.exceptions import ClientError

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

AWS_REGION = 'us-east-1'
vpc_client = boto3.client('ec2',
        aws_access_key_id='AKIAR35F7LDGLHXOJASY',
        aws_secret_access_key='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')

vpc_resource = boto3.resource("ec2", region_name=AWS_REGION)

def return_vpc_param():
    """
    Return parameters of default VPC.
    """
    vpc_client = boto3.client('ec2',
        aws_access_key_id='AKIAR35F7LDGLHXOJASY',
        aws_secret_access_key='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')
    try:
        #logger.info(f'Describing VPC...')
        response = vpc_client.describe_vpcs()
    except ClientError as e:
        logger.exception(f'Could not describe VPC : {e}')
        #pprint(vpc_client.describe_vpcs()['Vpcs'])
    for elem in vpc_client.describe_vpcs()['Vpcs']:
        if elem.get('InstanceTenancy') == 'default':
            return elem.get('VpcId')

my_session = boto3.session.Session()
my_region = my_session.region_name

print(my_region)
print(return_vpc_param())
vpc_resource = boto3.resource("ec2", region_name = 'us-west-1')


def create_security_group(description, groupname, vpc_id):
    """
    Creates a security group with the specified configuration.
    """
    try:
        response = vpc_resource.create_security_group(
                                                    GroupName=groupname,
                                                    VpcId=vpc_id)
    except ClientError:
        logger.exception('Could not create a security group.')
        raise
    else:
        return response


DESCRIPTION = 'Authorise redshift cluster access'
GROUPNAME = 'redshift_security_group1'
VPC_ID = return_vpc_param()
logger.info(f'Creating a security group...')
security_group = create_security_group(DESCRIPTION, GROUPNAME, VPC_ID)
logger.info(f'Security group created with ID: {security_group.id}')
