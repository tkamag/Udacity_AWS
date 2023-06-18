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

# Script generated for node Customer Curated
CustomerCurated_node1677211594534 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://udacity-project-lake-house/customer/curated/"],
        "recurse": True,
    },
    transformation_ctx="CustomerCurated_node1677211594534",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://udacity-project-lake-house/step_trainer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerTrusted_node1",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1677211516686 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://udacity-project-lake-house/accelerometer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerTrusted_node1677211516686",
)

# Script generated for node Distinct User Email
DistinctUserEmail_node1677211642582 = awsglue.dynamicframe.fromDF(
    CustomerCurated_node1677211594534.toDF().dropDuplicates(["email", "serialNumber"]),
    glueContext,
    "DistinctUserEmail_node1677211642582",
)

# Script generated for node Join User to Serial Number
JoinUsertoSerialNumber_node1677211732521 = Join.apply(
    frame1=AccelerometerTrusted_node1677211516686,
    frame2=DistinctUserEmail_node1677211642582,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="JoinUsertoSerialNumber_node1677211732521",
)

# Script generated for node Drop Customer Fields
DropCustomerFields_node1677211894771 = DropFields.apply(
    frame=JoinUsertoSerialNumber_node1677211732521,
    paths=[
        "birthDay",
        "registrationDate",
        "shareWithResearchAsOfDate",
        "customerName",
        "email",
        "lastUpdateDate",
        "phone",
        "shareWithFriendsAsOfDate",
        "shareWithPublicAsOfDate",
    ],
    transformation_ctx="DropCustomerFields_node1677211894771",
)

# Script generated for node Rename Serial Number Field
RenameSerialNumberField_node1677211942989 = RenameField.apply(
    frame=DropCustomerFields_node1677211894771,
    old_name="serialNumber",
    new_name="accelerometer_serialnumber",
    transformation_ctx="RenameSerialNumberField_node1677211942989",
)

# Script generated for node Join to Accelerometer
JointoAccelerometer_node2 = Join.apply(
    frame1=StepTrainerTrusted_node1,
    frame2=RenameSerialNumberField_node1677211942989,
    keys1=["serialNumber", "sensorReadingTime"],
    keys2=["accelerometer_serialnumber", "timeStamp"],
    transformation_ctx="JointoAccelerometer_node2",
)

# Script generated for node Drop Accelerometer Fields
DropAccelerometerFields_node1677211995987 = DropFields.apply(
    frame=JointoAccelerometer_node2,
    paths=["accelerometer_serialnumber", "sensorReadingTime"],
    transformation_ctx="DropAccelerometerFields_node1677211995987",
)

# Script generated for node Machine Learning Curated
MachineLearningCurated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropAccelerometerFields_node1677211995987,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://udacity-project-lake-house/step_trainer/machine_learning_curated/",
        "partitionKeys": [],
    },
    transformation_ctx="MachineLearningCurated_node3",
)

job.commit()