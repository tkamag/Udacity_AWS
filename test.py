import boto3
import json
from pprint import pprint
import os

AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']

iam_client = boto3.client('iam',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

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

print(response["Role"]["RoleName"])

# 3. Finally attach the policy to the new created role
resp = iam_client.attach_role_policy(
    RoleName='myRedshiftRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)

pprint(resp)
#print(json.loads(response))
