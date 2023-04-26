import boto3
import logging
import boto3
from botocore.exceptions import ClientError
import json
import os

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_REGION=os.environ['DEFAULT_REGION']

def create_ingress_rule(security_group_id):
    """
    Creates a security group ingress rule with the specified configuration.
    """

    vpc_client = boto3.client("ec2",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)

    try:
        response = vpc_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[{
                'IpProtocol': 'tcp',
                'FromPort': 5439,
                'ToPort': 5439,
                'IpRanges': [{
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'Allow traffic from anywhere in the world'
                }]
            }, ]
        )
    except ClientError:
        logger.exception('Could not create ingress security group rule.')
        raise
    else:
        return response.get('SecurityGroupRules', '')[0].get('SecurityGroupRuleId', '')


def create_security_group(description, groupname, vpc_id):
    """
    Creates a security group with the specified configuration.
    """

    ec2_client = boto3.client("ec2",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)
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
        if elem.get('InstanceTenancy') == 'default':
            return elem.get('VpcId')


def modify_rule(security_group_id, security_group_rule_id):
    """
    Modify the existing security group rules with the specified configuration.
    """
    vpc_client = boto3.client('ec2',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)

    try:
        response = vpc_client.modify_security_group_rules(
            GroupId=security_group_id,
            SecurityGroupRules=[
                {
                    'SecurityGroupRuleId': security_group_rule_id,
                    'SecurityGroupRule': {
                        'IpProtocol': '-1',
                        'FromPort': -1,
                        'ToPort': -1,
                        'CidrIpv4': '0.0.0.0/0',
                        'Description': 'Allow traffic to anywhere.'
                    }
                },
            ])
    except ClientError:
        logger.exception('Could not modify security group rule.')
        raise
    else:
        return response.get('ResponseMetadata', '').get('HTTPStatusCode', '')


if __name__ == '__main__':
    # Constants
    DESCRIPTION = 'Authorise redshift cluster access'
    GROUPNAME = 'redshift_security_group1'
    VPC_ID = return_vpc_param()
 
    logger.info(f'Reading Default VPC ID...')
    logger.info(f'Default VPC ID: \t {return_vpc_param()}')
    logger.info(f'Creating a security group...')
    SECURITY_GROUP_ID = create_security_group(DESCRIPTION, GROUPNAME, VPC_ID)
    logger.info(
        f'Security group created with ID: \t {json.dumps(SECURITY_GROUP_ID, indent=4)}')
    logger.info(f'Creating a security group ingress rule...')
    rule = create_ingress_rule(SECURITY_GROUP_ID)
    logger.info(
        f'security group ingress rule created: \t {json.dumps(rule, indent=4)}')
    logger.info(f'Modifing a security group rule...')
    SECURITY_GROUP_RULE_ID = rule
    _rule = modify_rule(SECURITY_GROUP_ID, SECURITY_GROUP_RULE_ID)
    logger.info(
        f'Security group rule modified with status code: \t {json.dumps(_rule, indent=4)}')
