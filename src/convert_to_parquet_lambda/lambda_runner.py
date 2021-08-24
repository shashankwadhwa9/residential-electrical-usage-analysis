import boto3
import os
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
GLUE_DATABASE = os.getenv('GLUE_DATABASE')
DATA_BUCKET = os.getenv('DATA_BUCKET')

# Create athena client
athena_client = boto3.client('athena')


def lambda_handler(event, context):
    """
    Convert the raw data to Parquet using CTAS statement
    """
    logger.info(f'Lambda execution started with event {event}')

    # Validate the event dict for required parameters
    required_fields = ['parquet_glue_table', 'raw_glue_table', 'partition_by_column']
    for field in required_fields:
        if not event.get(field):
            raise ValueError(f'"{field}" is required in the event')

    parquet_glue_table = event.get('parquet_glue_table')
    raw_glue_table = event.get('raw_glue_table')
    partition_by_column = event.get('partition_by_column')

    query = \
        f" CREATE TABLE IF NOT EXISTS {GLUE_DATABASE}.{parquet_glue_table} " \
        "  WITH ( " \
        "     format = 'PARQUET', " \
        "     parquet_compression = 'SNAPPY', " \
        f"    partitioned_by = ARRAY['{partition_by_column}'], " \
        f"    external_location = 's3://{DATA_BUCKET}/{parquet_glue_table}' " \
        ") AS " \
        "  SELECT * " \
        f" FROM {GLUE_DATABASE}.{raw_glue_table};"

    logger.info(query)

    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': GLUE_DATABASE
        },
        ResultConfiguration={
            'OutputLocation': f's3://{DATA_BUCKET}/tmp/{parquet_glue_table}'
        },
        WorkGroup='primary'
    )

    logger.info('Lambda execution completed')

    return response
