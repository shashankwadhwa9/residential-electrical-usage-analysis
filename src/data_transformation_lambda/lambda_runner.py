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

SENSORS = [f's_{i:02d}' for i in range(1, 11)]
OUTPUT_DIR = 'etl_tmp_output_parquet'


def _run_athena_query(args):
    for sensor in SENSORS:
        query = \
            "INSERT INTO " + GLUE_DATABASE + "." + OUTPUT_DIR + " " \
            "WITH " \
            "    t1 AS " \
            "        (SELECT d.loc_id, d.ts, d.data." + sensor + " AS kwh, l.state, l.tz " \
            "        FROM smart_hub_data_catalog.smart_hub_data_parquet d " \
            "        LEFT OUTER JOIN smart_hub_data_catalog.smart_hub_locations_parquet l " \
            "            ON d.loc_id = l.hash " \
            "        WHERE d.loc_id = '" + args['loc_id'] + "' " \
            "            AND d.dt BETWEEN cast('" + args['start_date'] + \
            "' AS date) AND cast('" + args['end_date'] + "' AS date)), " \
            "    t2 AS " \
            "        (SELECT at_timezone(from_unixtime(t1.ts, 'UTC'), t1.tz) AS ts, " \
            "             date_format(at_timezone(from_unixtime(t1.ts, 'UTC'), t1.tz), '%H') AS rate_period, " \
            "             m.description AS device, m.location, t1.loc_id, t1.state, t1.tz, t1.kwh " \
            "        FROM t1 LEFT OUTER JOIN smart_hub_data_catalog.sensor_mappings_parquet m " \
            "            ON t1.loc_id = m.loc_id " \
            "        WHERE t1.loc_id = '" + args['loc_id'] + "' " \
            "            AND m.state = t1.state " \
            "            AND m.description = (SELECT m2.description " \
            "                FROM smart_hub_data_catalog.sensor_mappings_parquet m2 " \
            "                WHERE m2.loc_id = '" + args['loc_id'] + "' AND m2.id = '" + sensor + "')), " \
            "    t3 AS " \
            "        (SELECT substr(r.to, 1, 2) AS rate_period, r.type, r.rate, r.year, r.month, r.state " \
            "        FROM smart_hub_data_catalog.electricity_rates_parquet r " \
            "        WHERE r.year BETWEEN cast(date_format(cast('" + args['start_date'] + \
            "' AS date), '%Y') AS integer) AND cast(date_format(cast('" + args['end_date'] + \
            "' AS date), '%Y') AS integer)) " \
            "SELECT replace(cast(t2.ts AS VARCHAR), concat(' ', t2.tz), '') AS ts, " \
            "    t2.device, t2.location, t3.type, t2.kwh, t3.rate AS cents_per_kwh, " \
            "    round(t2.kwh * t3.rate, 4) AS cost, t2.state, t2.loc_id " \
            "FROM t2 LEFT OUTER JOIN t3 " \
            "    ON t2.rate_period = t3.rate_period " \
            "WHERE t3.state = t2.state " \
            "ORDER BY t2.ts, t2.device;"

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


def lambda_handler(event, context):
    # Validate the event dict for required parameters
    required_fields = ['loc_id', 'start_date', 'end_date']
    for field in required_fields:
        if not event.get(field):
            raise ValueError(f'"{field}" is required in the event')

    loc_id = event.get('loc_id')
    start_date = event.get('start_date')
    end_date = event.get('end_date')

    # Run Athena query
    args = {
        'loc_id': loc_id,
        'start_date': start_date,
        'end_date': end_date
    }
    _run_athena_query(args)

    return {
        'statusCode': 200,
        'body': json.dumps({'status': 200})
    }
