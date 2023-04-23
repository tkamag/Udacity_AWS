import boto3
from botocore.exceptions import ClientError
import json


client = boto3.client("ec2",
                    aws_access_key_id='AKIAR35F7LDGLHXOJASY',
                    aws_secret_access_key='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')
client_log = boto3.client('logs')

for vpcid in client.describe_vpcs()['Vpcs']:
    vpc_id = vpcid['VpcId']
    print(vpc_id)

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


response = client.create_security_group(
    Description='My security group2',
    GroupName='my-security-group3',
    VpcId=return_vpc_param(),
)


print(json.dumps(response, indent=4))