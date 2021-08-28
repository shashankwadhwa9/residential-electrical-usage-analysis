SCRIPT_BUCKET="shashank-smart-hub-scripts"

# Create package zip for lambda
rm package2.zip
cd src/data_transformation_lambda/ && zip -r ../../package2.zip lambda_runner.py

# Push lambda package on S3
cd ../../
aws s3 cp package2.zip s3://${SCRIPT_BUCKET}/lambdas/smarthub-data-transformation/

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

echo "Run the lambda"
aws lambda invoke \
    --function-name smarthub-data-transformation \
    --payload '{"loc_id": "b6a8d42425fde548", "start_date": "2019-12-21", "end_date": "2019-12-22"}' \
    /dev/stdout
