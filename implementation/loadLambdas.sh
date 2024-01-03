ACCOUNTID=$(aws sts get-caller-identity --query "Account" --output text)
aws s3api create-bucket --bucket aws-sc-code-$ACCOUNTID --region us-east-1 
aws s3 cp lambdas/AWS_SC_Bedrock.zip s3://aws-sc-code-$ACCOUNTID/aws-sc-bedrock.zip      
aws s3 cp lambdas/AWS_SC_TransactionalData.zip s3://aws-sc-code-$ACCOUNTID/aws-sc-transactional-data-gen.zip      
aws s3 cp lambdas/AWS_SC_MasterData.zip s3://aws-sc-code-$ACCOUNTID/aws-sc-master-data-gen.zip      
aws s3 cp lambdas/getS3_objects.zip s3://aws-sc-code-$ACCOUNTID/getS3_objects.zip 

aws s3api create-bucket --bucket aws-sc-layers-$ACCOUNTID --region us-east-1 
aws s3 cp layers/boto3-layer.zip s3://aws-sc-layers-$ACCOUNTID/python.zip 

