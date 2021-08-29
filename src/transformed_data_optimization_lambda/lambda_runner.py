import boto3
import os
import logging
import json

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
GLUE_DATABASE = os.getenv('GLUE_DATABASE')
DATA_BUCKET = os.getenv('DATA_BUCKET')

# Create athena client
athena_client = boto3.client('athena')

INPUT_DIR = 'etl_tmp_output_parquet'
OUTPUT_DIR = 'etl_output_parquet'


def lambda_handler(event, context):
    query = \
        "CREATE TABLE IF NOT EXISTS " + GLUE_DATABASE + "." + OUTPUT_DIR + " " \
        "WITH ( " \
        "    format = 'PARQUET', " \
        "    parquet_compression = 'SNAPPY', " \
        "    partitioned_by = ARRAY['loc_id'], " \
        "    bucketed_by = ARRAY['state'], " \
        "    bucket_count = 1, " \
        "    external_location = 's3://" + DATA_BUCKET + "/" + OUTPUT_DIR + "' " \
        ") AS " \
        "SELECT * " \
        "FROM " + GLUE_DATABASE + "." + INPUT_DIR + ";"

    logger.info(query)

    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': GLUE_DATABASE
        },
        ResultConfiguration={
            'OutputLocation': f's3://{DATA_BUCKET}/tmp/{OUTPUT_DIR}'
        },
        WorkGroup='primary'
    )

    logger.info(response)

    return {
        'statusCode': 200,
        'body': json.dumps({'status': 200})
    }
