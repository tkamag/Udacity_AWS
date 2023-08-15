#!/bin/bash
# Define airflow connections to AWS
#
airflow connections add aws_credentials --conn-uri 'aws://AKIAWYJLQDEYHKUP5W2F:yM5azGRupWTwdLAhIJQilLOOsSQItktdADo%2F1Iuq@'
#
# Define redshift serverless cluster
#
airflow connections add redshift --conn-uri 'redshift://airflowuseraws:2MZsWrQuBCTV%23C7BdqiPi@default.464484571440.us-east-1.redshift-serverless.amazonaws.com:5439/dev'
#
# Define the Bucket
#
airflow variables set s3_bucket tka-udacity
#
# Define the prefix
#
airflow variables set s3_prefix data-pipelines