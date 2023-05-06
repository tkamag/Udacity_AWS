# Project Introduction
## Project: Data Warehouse

### Introduction

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to.

<p align="center">
  <img src="./fig/sparkify-s3-to-redshift-etl.png" alt=".." title="Optional title" width="66%" height="70%"/>  
</p> 

<p align="center">
  <caption>System Architecture for AWS S3 to Redshift ETL</caption>  
</p> 