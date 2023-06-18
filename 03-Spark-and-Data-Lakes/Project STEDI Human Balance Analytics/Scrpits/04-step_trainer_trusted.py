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

# Script generated for node customer_curated
customer_curated_node1686940912758 = glueContext.create_dynamic_frame.from_catalog(
    database="udacity_project_db",
    table_name="customer_curated",
    transformation_ctx="customer_curated_node1686940912758",
)

# Script generated for node step_trainer
step_trainer_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://udacity-project-lake-house/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="step_trainer_node1",
)

# Script generated for node Join
Join_node1686940939588 = Join.apply(
    frame1=customer_curated_node1686940912758,
    frame2=step_trainer_node1,
    keys1=["serialnumber"],
    keys2=["serialNumber"],
    transformation_ctx="Join_node1686940939588",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=Join_node1686940939588,
    mappings=[
        ("customername", "string", "customername", "string"),
        ("email", "string", "email", "string"),
        ("phone", "string", "phone", "string"),
        ("birthday", "string", "birthday", "string"),
        ("serialnumber", "string", "serialnumber", "string"),
        ("registrationdate", "long", "registrationdate", "long"),
        ("lastupdatedate", "long", "lastupdatedate", "long"),
        ("sharewithresearchasofdate", "long", "sharewithresearchasofdate", "long"),
        ("sharewithpublicasofdate", "long", "sharewithpublicasofdate", "long"),
        ("sharewithfriendsasofdate", "long", "sharewithfriendsasofdate", "long"),
        ("sensorReadingTime", "bigint", "sensorReadingTime", "long"),
        ("serialNumber", "string", "serialNumber", "string"),
        ("distanceFromObject", "int", "distanceFromObject", "int"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node step_trainer_trusted
step_trainer_trusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMapping_node2,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://udacity-project-lake-house/step_trainer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="step_trainer_trusted_node3",
)

job.commit()
