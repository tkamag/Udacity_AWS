# A. Project Instructions

In this project, using ``AWS Glue, AWS S3, Python, and Spark``, we are going to create or generate Python scripts to build a **machine learning** table that satisfies these requirements from the **STEDI** data scientists.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time. Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes. Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model.

As a data engineer on the STEDI Step Trainer team, I will extract the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS so that Data Scientists can train the learning model by creating 05 AWS Glue Jobs.

# B. Files and Screenshots
## B.1 Customer trusted
Here, we will create a Python script that sanitize the Customer data from the Website (Landing Zone) and only store the Customer Records who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called ``customer_trusted``.

* [customer_landing.sql](./Scrpits/01-customer_landing.sql)

<p align="center">
  <img src="./fig/01-customer_landing.png" alt=".." title="Optional title" width="96%" height="70%"/>  
</p> 
<p align="center">
  <caption>Customer Landing</caption>  
</p> 
