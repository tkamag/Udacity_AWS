import boto3
import logging
import boto3
from botocore.exceptions import ClientError
import json
AWS_REGION = 'us-east-2'
# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')
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

def create_security_group(description, groupname, vpc_id):
    """
    Creates a security group with the specified configuration.
    """

    ec2_client = boto3.client("ec2",
                    aws_access_key_id='AKIAR35F7LDGLHXOJASY',
                    aws_secret_access_key='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')
    try:
        response = ec2_client.create_security_group(
                    Description=description,
                    GroupName=groupname,
                    VpcId=return_vpc_param(),
                                    TagSpecifications=[{
                                        'ResourceType': 'security-group',
                                        'Tags': [{
                                                'Key':  'Name',
                                                'Value':    groupname}]}])
    except ClientError:
        logger.exception('Could not create a security group.')
        raise
    else:
        return response.get('GroupId', '')

if __name__ == '__main__':
    # Constants
    DESCRIPTION = 'Authorise redshift cluster access'
    GROUPNAME = 'redshift_security_group2'
    logger.info(f'Reading Default VPC ID...')
    logger.info(f'Default VPC ID: \t {return_vpc_param()}')
    VPC_ID=return_vpc_param()
    logger.info(f'Creating a security group...')
    security_group = create_security_group(DESCRIPTION, GROUPNAME, VPC_ID)
    logger.info(f'Security group created with ID: \t {json.dumps(security_group, indent=4)}')