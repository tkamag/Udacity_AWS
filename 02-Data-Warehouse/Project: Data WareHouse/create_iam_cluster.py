import boto3
import json
import psycopg2
import configparser
import logging
import pandas as pd
from pprint import pprint

from botocore.exceptions import ClientError


# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def create_iam_role(iam_client, DWH_IAM_ROLE_NAME):
    '''
    Creates IAM Role for Redshift, to allow it to use AWS services
    '''
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
    try:
        logger.info("1.1 Creating a new IAM Role")
        dwhRole = iam_client.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description=DESCRIPTION,
            AssumeRolePolicyDocument=assume_policy
        )
    except Exception as e:
        logger.info(f'Exeption: {e}')

    logger.info("1.2 Attaching Policy")

    iam_client.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                                  PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                                  )['ResponseMetadata']['HTTPStatusCode']

    logger.info("1.3 Get the IAM role ARN")
    roleArn = iam_client.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

    return roleArn


def create_cluster(redshift, roleArn, DWH_CLUSTER_TYPE, DWH_NODE_TYPE, DWH_NUM_NODES, DWH_DB, DWH_CLUSTER_IDENTIFIER, DWH_DB_USER, DWH_DB_PASSWORD):
    '''
    Creates Redshift cluster with default Virtual Private Cloud (VPC)
    '''

    try:
        response = redshift.create_cluster(
            # HW
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),

            # Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,

            IamRoles=[roleArn]
        )
    except Exception as e:
        print(e)


def return_cluster_props(redshift, DWH_CLUSTER_IDENTIFIER):
    '''
    Retrieve design Redshift clusters properties
    '''

    def prettyRedshiftProps(props):
        pd.set_option('display.max_colwidth', None)
        keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus",
                      "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
        x = [(k, v) for k, v in props.items() if k in keysToShow]
        return pd.DataFrame(data=x, columns=["Key", "Value"])

    # Waiter is use for waiting the availability of the Redhift Cluster

    waiter = redshift.get_waiter('cluster_available')

    waiter.wait(
        ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
        WaiterConfig={
            'Delay': 30,
            'MaxAttempts': 6})
    waiter = redshift.get_waiter('cluster_available')
    myClusterProps = redshift.describe_clusters(
        ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]

    DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
    DWH_ROLE_ARN = myClusterProps['IamRoles'][0]['IamRoleArn']

    return myClusterProps, prettyRedshiftProps(myClusterProps), DWH_ENDPOINT, DWH_ROLE_ARN


def open_sg_ports(ec2, myClusterProps, DWH_PORT):
    '''
    Update clusters security group to allow access through redshift port
    '''

    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        print(defaultSg)
        defaultSg.authorize_ingress(
            GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # Constants
    DESCRIPTION = "Allows Redshift clusters to call AWS services on your behalf."
    GROUPNAME = 'redshift_security_group2'

    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    ACCESS_KEY = config.get('AWS', 'ACCESS_KEY')
    SECRET_KEY = config.get('AWS', 'SECRET_KEY')
    ACCESS_REGION = config.get('AWS', 'ACCESS_REGION')

    DWH_CLUSTER_TYPE = config.get("CLUSTER_PRO", "DWH_CLUSTER_TYPE")
    DWH_NUM_NODES = config.get("CLUSTER_PRO", "DWH_NUM_NODES")
    DWH_NODE_TYPE = config.get("CLUSTER_PRO", "DWH_NODE_TYPE")
    DWH_CLUSTER_IDENTIFIER = config.get(
        "CLUSTER_PRO", "DWH_CLUSTER_IDENTIFIER")

    DWH_DB = config.get("CLUSTER", "DB_NAME")
    DWH_DB_USER = config.get("CLUSTER", "DB_USER")
    DWH_DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
    DWH_PORT = config.get("CLUSTER", "DB_PORT")
    DWH_HOST = config.get("CLUSTER", "HOST")

    DWH_IAM_ROLE_NAME = config.get("IAM_ROLE", "DWH_IAM_ROLE_NAME")
    DWH_ARN = config.get("IAM_ROLE", "DWH_ARN")

    (DWH_DB_USER, DWH_DB_PASSWORD, DWH_DB)

    df = pd.DataFrame({"Param": ["DWH_CLUSTER_TYPE", "DWH_NUM_NODES", "DWH_NODE_TYPE", "DWH_CLUSTER_IDENTIFIER",
                                 "DWH_DB", "DWH_DB_USER", "DWH_DB_PASSWORD", "DWH_PORT", "DWH_IAM_ROLE_NAME"],
                       "Value": [DWH_CLUSTER_TYPE, DWH_NUM_NODES, DWH_NODE_TYPE, DWH_CLUSTER_IDENTIFIER,
                                 DWH_DB, DWH_DB_USER, DWH_DB_PASSWORD, DWH_PORT, DWH_IAM_ROLE_NAME]})

    ec2 = boto3.resource('ec2',
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         region_name=ACCESS_REGION)

    s3 = boto3.resource('s3',
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY,
                        region_name=ACCESS_REGION)

    iam = boto3.client('iam',
                       aws_access_key_id=ACCESS_KEY,
                       aws_secret_access_key=SECRET_KEY,
                       region_name=ACCESS_REGION)

    redshift = boto3.client('redshift',
                            aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=ACCESS_REGION)

    arn = create_iam_role(iam, DWH_IAM_ROLE_NAME)
    logger.info(
        f'IAM role created with ID:  {arn}')

    # Creating Redshift Cluster

    logger.info(f'Creating Redshift Cluster...')
    create_cluster(redshift, arn, DWH_CLUSTER_TYPE, DWH_NODE_TYPE,
                   DWH_NUM_NODES, DWH_DB, DWH_CLUSTER_IDENTIFIER, DWH_DB_USER, DWH_DB_PASSWORD)
    myClusterProps, _myClusterProps, DWH_ENDPOINT, DWH_ROLE_ARN = return_cluster_props(
        redshift, DWH_CLUSTER_IDENTIFIER)
    logger.info(
        f'Redshift Cluster endpoint: {DWH_ENDPOINT}')
    logger.info(
        f'Redshift Cluster arn:\t{DWH_ROLE_ARN}')
    logger.info(f'Redshift Cluster {DWH_CLUSTER_IDENTIFIER} was created !!!')

    logger.info(f'Update clusters security group...')
    logger.info(
        f'{open_sg_ports(ec2, _myClusterProps, DWH_PORT)}'
    )
    conn_string = "postgresql://{}:{}@{}:{}/{}".format(
        DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB)
    logger.info(
        f'{conn_string}'
    )
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
            *config['CLUSTER'].values()))
        cur = conn.cursor()
        logger.info(f"Connected to the Cluster for testing.")
        logger.info(f"Connection OK.!!!")
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(f'{error}')
        logger.info(f"Something wrong with your Connection....")
