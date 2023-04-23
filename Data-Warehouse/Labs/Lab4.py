import logging
import boto3
from botocore.exceptions import ClientError
import json
AWS_REGION = 'us-east-1'
# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')
vpc_client = boto3.client("ec2", region_name=AWS_REGION,
        aws_access_key_id='AKIAR35F7LDGLHXOJASY',
        aws_secret_access_key='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')

def describe_vpc_attribute(vpc_id, attribute):
    """
    Describes the specified attribute of the specified VPC.
    """
    try:
        response = vpc_client.describe_vpc_attribute(Attribute=attribute,
                                                    VpcId=vpc_id)
    except ClientError:
        logger.exception('Could not describe a vpc attribute.')
        raise
    else:
        return response

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

if __name__ == '__main__':
    # Constants
    VPC_ID=return_vpc_param()
    ATTRIBUTE = 'enableDnsSupport'
    custom_vpc_attribute = describe_vpc_attribute(VPC_ID, ATTRIBUTE)
    logger.info(
        f'VPC attribute details: \n{json.dumps(custom_vpc_attribute, indent=4)}'
    )