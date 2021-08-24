SCRIPT_BUCKET="shashank-smart-hub-scripts"

# Create package zip for lambda
rm package.zip
cd src/convert_to_parquet_lambda/ && zip -r ../../package.zip lambda_runner.py

# Push lambda package on S3
cd ../../
aws s3 cp package.zip s3://${SCRIPT_BUCKET}/lambdas/smarthub-raw-data-to-parquet/

# Update the stack with the new lambda resource
set +e
update_output=$( aws cloudformation update-stack \
  --stack-name residential-electrical-usage-analysis \
  --template-body file://cfn/cftemplate.json \
  --parameters file://cfn/parameters.json \
  --capabilities CAPABILITY_NAMED_IAM  2>&1)
status=$?
set -e

echo "$update_output"

if [ $status -ne 0 ] ; then

  # Don't fail for no-op update
  if [[ $update_output == *"ValidationError"* && $update_output == *"No updates"* ]] ; then
    echo -e "\nFinished create/update - no updates to be performed"
    exit 0
  else
    exit $status
  fi

fi

echo "Waiting for stack update to complete ..."
aws cloudformation wait stack-update-complete \
  --region ap-south-1 \
  --stack-name residential-electrical-usage-analysis \
