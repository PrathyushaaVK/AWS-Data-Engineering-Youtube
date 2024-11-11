import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1731268926647 = glueContext.create_dynamic_frame.from_catalog(database="yt_project_cleaned", table_name="raw_statistics", transformation_ctx="AWSGlueDataCatalog_node1731268926647")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1731268924085 = glueContext.create_dynamic_frame.from_catalog(database="yt_project_cleaned", table_name="cleaned_statistics_reference_data", transformation_ctx="AWSGlueDataCatalog_node1731268924085")

# Script generated for node Join
Join_node1731268966351 = Join.apply(frame1=AWSGlueDataCatalog_node1731268926647, frame2=AWSGlueDataCatalog_node1731268924085, keys1=["category_id"], keys2=["id"], transformation_ctx="Join_node1731268966351")

# Script generated for node Amazon S3
AmazonS3_node1731269022803 = glueContext.getSink(path="s3://youtube-data-engg-project-analytics", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["region", "category_id"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1731269022803")
AmazonS3_node1731269022803.setCatalogInfo(catalogDatabase="yt_project_analytics",catalogTableName="final_analytics")
AmazonS3_node1731269022803.setFormat("glueparquet", compression="snappy")
AmazonS3_node1731269022803.writeFrame(Join_node1731268966351)
job.commit()