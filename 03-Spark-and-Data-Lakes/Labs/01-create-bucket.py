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
                          region_name=AWS_REGION,
                          aws_session_token=AWS_SESSION_TOKEN)

    try:
        response = client.create_bucket(
                        Bucket='examplebucket',
                        CreateBucketConfiguration={
                        'LocationConstraint': 'eu-east-1',
                },
            )
    except Exception as e:
        logger.info(f'Exeption: {e}')
    return response

if __name__ == '__main__':
    # Constants
    BUCKET_NAME='tka-lake-house'
    a=create_a_bucket()
    logger.info(f'Creating a Bucket...')
 
    logger.info(
        f'\nBucket created with:  \nName: \t {a}')
    logger.info(f'Bucket Created...')
