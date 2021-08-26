aws lambda invoke \
    --function-name smarthub-raw-data-to-parquet \
    --payload '{"parquet_glue_table": "smart_hub_data_parquet", "raw_glue_table": "smart_hub_data_json", "partition_by_column": "dt"}' \
    /dev/stdout

aws lambda invoke \
    --function-name smarthub-raw-data-to-parquet \
    --payload '{"parquet_glue_table": "sensor_mappings_parquet", "raw_glue_table": "sensor_mappings_json", "partition_by_column": "state"}' \
    /dev/stdout

aws lambda invoke \
    --function-name smarthub-raw-data-to-parquet \
    --payload '{"parquet_glue_table": "smart_hub_locations_parquet", "raw_glue_table": "smart_hub_locations_csv", "partition_by_column": "state"}' \
    /dev/stdout
