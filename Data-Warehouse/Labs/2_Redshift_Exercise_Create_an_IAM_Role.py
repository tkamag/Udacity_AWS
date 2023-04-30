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
AWS_SESSION_TOKEN=os.environ['AWS_SESSION_TOKEN']

def create_iam_role():
    """
        Create an IAM role
    """
    iam_client = boto3.client('iam',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          aws_session_token=AWS_SESSION_TOKEN)

# To createe an IAM role ypou will need
# 1. Define policy that will be attach to a role

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
                        "redshift.amazonaws.com"
                    ]
                }
            }
        ]
    })

# 2. Create role with its name and policy

    response = iam_client.create_role(
        RoleName='myRedshiftRole',
        AssumeRolePolicyDocument=assume_policy)

    #print(response["Role"]["RoleName"])
    #print(response["Role"])

# 3. Finally attach the policy to the new created role
    resp = iam_client.attach_role_policy(
        RoleName='myRedshiftRole',
        PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
    )
    return (response["Role"]['RoleName'], response["Role"]['Arn'])

if __name__ == '__main__':
    # Constants
    a=create_iam_role()
    logger.info(f'Creating An IAM Role...')
 
    logger.info(
        f'\nIAM created with:  \nName: \t {a[0]} \nArn: \t {a[1]}')
    logger.info(f'IAM Role Created...')
