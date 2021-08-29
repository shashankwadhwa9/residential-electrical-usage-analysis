DATA_BUCKET="shashank-smart-hub-data"
SCRIPT_BUCKET="shashank-smart-hub-scripts"
LOG_BUCKET="shashank-smart-hub-logs"

# delete s3 contents first
aws s3 rm s3://${DATA_BUCKET} --recursive
aws s3 rm s3://${SCRIPT_BUCKET} --recursive
aws s3 rm s3://${LOG_BUCKET} --recursive

# delete stack
aws cloudformation delete-stack --stack-name residential-electrical-usage-analysis
