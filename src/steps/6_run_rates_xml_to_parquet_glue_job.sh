SCRIPT_BUCKET="shashank-smart-hub-scripts"

# Copy the file to S3
aws s3 cp src/rates_xml_to_parquet_glue_job/main.py s3://${SCRIPT_BUCKET}/glue_scripts/rates_xml_to_parquet.py

# Run the Glue job
aws glue start-job-run --job-name rates-xml-to-parquet

# Run the crawler
aws glue start-crawler --name smart-hub-rates-parquet
