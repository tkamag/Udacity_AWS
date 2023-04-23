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

def create_ingress_rule(security_group_id):
    """
    Creates a security group ingress rule with the specified configuration.
    """

    vpc_client = boto3.client("ec2",
                    aws_access_key_id='AKIAR35F7LDGLHXOJASY',
                    aws_secret_access_key='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')

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


def create_egress_rule(security_group_id):
    """
    Creates a security group egress rule with the specified configuration.
    """
    vpc_client = boto3.client('ec2',
                            aws_access_key_id='AKIAR35F7LDGLHXOJASY',
                            aws_secret_access_key='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')

    try:
        response = vpc_client.authorize_security_group_egress(
            GroupId=security_group_id,
            IpPermissions=[{
                'IpProtocol': '-1',
                'FromPort' : -1,
                'ToPort': -1,
#                'FromPort': '',
#                'ToPort': '',
                'IpRanges': [{
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'Allow traffic to anywhere.'
                }]
            }], )
    except ClientError:
        logger.exception('Could not create egress security group rule.')
        raise
    else:
        return response.get('SecurityGroupRules', '').get('SecurityGroupRuleId', '')

def modify_rule(security_group_id, security_group_rule_id):
    """
    Modify the existing security group rules with the specified configuration.
    """
    vpc_client = boto3.client('ec2',
                            aws_access_key_id='AKIAR35F7LDGLHXOJASY',
                            aws_secret_access_key='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')

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
        return response


if __name__ == '__main__':
    # Constants
    DESCRIPTION = 'Authorise redshift cluster access'
    GROUPNAME = 'redshift_security_group2'
    VPC_ID=return_vpc_param()
    SECURITY_GROUP_ID = create_security_group(DESCRIPTION, GROUPNAME, VPC_ID)
    SECURITY_GROUP_RULE_ID = create_egress_rule(SECURITY_GROUP_ID)
    logger.info(f'Reading Default VPC ID...')
    logger.info(f'Default VPC ID: \t {return_vpc_param()}')
    logger.info(f'Creating a security group...')
    #security_group = create_security_group(DESCRIPTION, GROUPNAME, VPC_ID)
    logger.info(f'Security group created with ID: \t {json.dumps(SECURITY_GROUP_ID, indent=4)}')
    logger.info(f'Creating a security group ingress rule...')
    rule = create_ingress_rule(SECURITY_GROUP_ID)
    logger.info(
        f'Security group ingress rule created: \t {json.dumps(rule, indent=4)}')

   # _rule = create_egress_rule(SECURITY_GROUP_ID)
   # logger.info(
   #     f'Security group egress rule created: \n{json.dumps(_rule, indent=4)}')

    logger.info(f'Modifing a security group rule...')
    rule = modify_rule(SECURITY_GROUP_ID, SECURITY_GROUP_RULE_ID)
    logger.info(
        f'Security group rule modified: \n{json.dumps(rule, indent=4)}')
