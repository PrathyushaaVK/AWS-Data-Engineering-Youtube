# YouTube Data Engineering and Analysis with AWS

This project builds a data pipeline on AWS to process and analyze YouTube trending video data from various regions. The pipeline automates data ingestion, transformation, and storage, facilitating insights into user engagement across multiple regions.

## Project Overview

YouTube provides trending video data across multiple regions, recording user interactions like views, likes, dislikes, and comments. This project organizes and analyzes data from these regions using AWS services, enabling visualization and querying of trends. Data is ingested from raw JSON and CSV files, cleansed, converted to Parquet format, and queried in Athena.

### Regions Covered
- For this project, the regions covered are United States (US), Great Britain (GB), Canada (CA)

### Dataset Structure
Each record includes:
- **Metadata**: `video_id`, `title`, `channel_title`, `publish_time`, `tags`
- **User Interaction**: `views`, `likes`, `dislikes`, `comment_count`
- **Other**: `category_id`, `description`

### AWS Architecture Overview

The project architecture includes the following components:

- **Amazon S3**: Stores raw and processed data.
- **AWS Glue**: Crawls raw data to catalog and preprocess it for analysis.
- **AWS Lambda**: Cleans JSON data, flattens nested fields, and converts data to Parquet format.
- **Amazon Athena**: Queries processed data for analysis.
- **Amazon QuickSight**: Visualizes trending video metrics across regions.

## Prerequisites

- **AWS CLI**: Configured with access credentials.
- **IAM Roles**: S3 and Glue permissions for data access and Lambda roles.
- **awswrangler**: Library for data transformation in Python (included as a Lambda layer).

---

## Setup and Execution Steps

### 1. Data Ingestion

- The project begins by collecting raw data in both JSON and CSV formats, containing information on trending YouTube videos across various regions.
- The raw data is uploaded to Amazon S3 for storage, with separate buckets for **raw** and **cleansed** data.
**Step 1:** AWS CLI Configuration

Configure the AWS CLI to manage services from the command line.

```bash
aws configure
```

**Step 2:** Create S3 Buckets

Create S3 buckets for raw data, cleansed data, and Athena output.

```bash
# Raw data bucket
aws s3 mb s3://youtube-data-engg-project

# Cleansed data bucket
aws s3 mb s3://youtube-data-engg-project-cleansed

# Athena query output bucket
aws s3 mb s3://youtube-data-engg-project-athena-job
```

**Step 3:** Upload Data to S3
Navigate to the dataset directory and upload JSON and CSV files to S3.

#### Upload JSON Files
```bash
aws s3 cp . s3://youtube-data-engg-project/youtube/raw_statistics_reference_data/ --recursive --exclude "*" --include "*.json"
```
#### Upload CSV Files
```bash
aws s3 cp CAvideos.csv s3://youtube-data-engg-project/youtube/raw_statistics/region=ca/
# Repeat for each CSV file (DE, FR, GB, IN, JP, KR, MX, RU, US)
```
### 2. Data Cataloging with AWS Glue

- An **AWS Glue crawler** is configured to scan the raw data in S3, identify and catalog the schema, and store this metadata in a Glue database.
- The Glue database serves as a centralized catalog for the raw data, making it easier to organize and query later.

### 3. Data Transformation with AWS Lambda

- A **Lambda function** is created to process JSON files by flattening nested data structures and converting them into a tabular format (**Apache Parquet**).
- The Lambda function automates data cleansing by converting JSON data into Parquet format and storing it in a designated S3 bucket for cleansed data.

### 4. Automated Data Processing

- A **Lambda trigger** is set up on S3 so that any new JSON file uploaded to the raw data bucket triggers the transformation function.
- This ensures real-time data processing as soon as new data is uploaded.

### 5. Data Joining with AWS Glue Job

- After the data is converted into Parquet format, a **Glue job** is set up to join the cleansed JSON and CSV Parquet data files into a consolidated dataset.
- The joined dataset is saved back into an S3 bucket, optimized for efficient querying.

### 6. Querying with Amazon Athena

- **Amazon Athena** is used to run SQL-like queries on the consolidated dataset stored in S3.
- This allows for analysis of key metrics such as the most viewed or liked videos by region.

### 7. Visualization with Amazon QuickSight

- The data is connected to **Amazon QuickSight** to create visual dashboards.
- These dashboards provide insights into metrics like engagement rates, popular channels, and the most-liked or disliked videos across regions.





