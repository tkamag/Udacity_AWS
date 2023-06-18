import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node customer_trusted
customer_trusted_node1686934074502 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://udacity-project-lake-house/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="customer_trusted_node1686934074502",
)

# Script generated for node accelerometer_landing
accelerometer_landing_node1686934364238 = glueContext.create_dynamic_frame.from_catalog(
    database="udacity_project_db",
    table_name="accelerometer_landing",
    transformation_ctx="accelerometer_landing_node1686934364238",
)

# Script generated for node Join
Join_node1686934020348 = Join.apply(
    frame1=customer_trusted_node1686934074502,
    frame2=accelerometer_landing_node1686934364238,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="Join_node1686934020348",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=Join_node1686934020348,
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
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node accelerometer_trusted
accelerometer_trusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMapping_node2,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://udacity-project-lake-house/customer/curated/",
        "partitionKeys": [],
    },
    transformation_ctx="accelerometer_trusted_node3",
)

job.commit()
