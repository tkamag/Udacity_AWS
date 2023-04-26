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
#1. Create user

def create_iam_user(username):
    """
    Creates an IAM user with AWS Management console access  for Redshift
    """
    iam_client = boto3.client('iam', 
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)

    response = iam_client.create_user(
        UserName=username
    )
    return (response.get('User', '').get('UserName',''), response.get('User', '').get('Arn',''))

# 2. Attach AmazonRedshiftFullAccess and AmazonS3ReadOnlyAccess to this new user

def attach_policy_user(username):
    """
    Attach specified managed policy
    AmazonRedshiftFullAccess: arn:aws:iam::aws:policy/AmazonRedshiftFullAccess
    AmazonS3ReadOnlyAccess:   arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
    """
    iam_client = boto3.client('iam', 
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)


    #user = iam_client.User(username)
    list_policy = ['arn:aws:iam::aws:policy/AmazonRedshiftFullAccess', 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess']
    for pol in list_policy:
        response = iam_client.attach_user_policy(
            UserName=username,
            PolicyArn=pol)
    #return(response)

def list_policy_user(username):
    """
        List User piolicies
    """
    iam_client = boto3.client('iam', 
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)


    #user = iam_client.User(username)

    response = iam_client.list_attached_user_policies(
            UserName=username)
    return(response.get('AttachedPolicies',''))

if __name__ == '__main__':
    # Constants
    USERNAME = 'test-conupdate-10'
    a=create_iam_user(USERNAME)
    logger.info(f'Creating username...')
    logger.info(f'\nUser:\t {a[0]} \nArn: \t {a[1]}')
    logger.info(f'User was created...')

    logger.info(f'Attaching policy(ies) to...:\t{a[0]}')
    logger.info(f'Policy details:\t {pprint(attach_policy_user(USERNAME))}')
    logger.info(f'Policy attached...')
    for item in list_policy_user(USERNAME):
        logger.info(f'\nPolicyName: { item["PolicyName"]} \nPolicyArn: {item["PolicyArn"]}')

