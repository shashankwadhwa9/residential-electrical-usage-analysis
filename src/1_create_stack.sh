if ! aws cloudformation describe-stacks --region ap-south-1 --stack-name residential-electrical-usage-analysis ; then

  echo -e "\nStack does not exist, creating ..."
  aws cloudformation create-stack \
    --stack-name residential-electrical-usage-analysis \
    --template-body file://cfn/cftemplate.json \
    --parameters file://cfn/parameters.json \
    --capabilities CAPABILITY_NAMED_IAM

  echo "Waiting for stack to be created ..."
  aws cloudformation wait stack-create-complete \
    --region ap-south-1 \
    --stack-name residential-electrical-usage-analysis \

else

  echo -e "\nStack exists, attempting update ..."

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

fi

echo "Finished create/update successfully!"