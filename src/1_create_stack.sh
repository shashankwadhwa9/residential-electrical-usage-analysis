aws cloudformation create-stack \
    --stack-name residential-electrical-usage-analysis \
    --template-body file://cfn/cftemplate.json \
    --parameters file://cfn/parameters.json \
    --capabilities CAPABILITY_NAMED_IAM