# Implementation Guide (us-east-1)
This implementation is based on AWS CloudFormation service, an Infrastructure As Code (IaaC) service. 

YOU MUST BE IN ***US-EAST-1*** REGION

### Step 1 
Copy the zip code into a new s3 bucket in your account.

1. Open the terminal
2. Run the following command:
```bash
sh loadLambdas.sh
```

This will create an S3 bucket named "aws-sc-code-{AWS-AccountID}". Inside this bucket, you will have 4 zip files that contains the code of the project. 
### Step 2
Create the infrastructure in AWS.
1. In the AWS Console go to IAM service
2. 