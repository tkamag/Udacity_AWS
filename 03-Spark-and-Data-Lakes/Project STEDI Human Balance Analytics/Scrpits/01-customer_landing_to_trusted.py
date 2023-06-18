import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node customer_landing
customer_landing_node1686924549264 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://udacity-project-lake-house/customer/landing/"],
        "recurse": True,
    },
    transformation_ctx="customer_landing_node1686924549264",
)

# Script generated for node Filter (Share Data)
FilterShareData_node1686842412158 = Filter.apply(
    frame=customer_landing_node1686924549264,
    f=lambda row: (not (row["shareWithResearchAsOfDate"] == 0)),
    transformation_ctx="FilterShareData_node1686842412158",
)

# Script generated for node Change Schema
ChangeSchema_node1686929501095 = ApplyMapping.apply(
    frame=FilterShareData_node1686842412158,
    mappings=[
        ("customerName", "string", "customerName", "string"),
        ("email", "string", "email", "string"),
        ("phone", "string", "phone", "string"),
        ("birthDay", "string", "birthDay", "string"),
        ("serialNumber", "string", "serialNumber", "string"),
        ("registrationDate", "bigint", "registrationDate", "bigint"),
        ("lastUpdateDate", "bigint", "lastUpdateDate", "bigint"),
        ("shareWithResearchAsOfDate", "bigint", "shareWithResearchAsOfDate", "bigint"),
        ("shareWithPublicAsOfDate", "bigint", "shareWithPublicAsOfDate", "bigint"),
        ("shareWithFriendsAsOfDate", "bigint", "shareWithFriendsAsOfDate", "bigint"),
    ],
    transformation_ctx="ChangeSchema_node1686929501095",
)

# Script generated for node customer Trusted
customerTrusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node1686929501095,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://udacity-project-lake-house/customer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="customerTrusted_node3",
)

job.commit()
