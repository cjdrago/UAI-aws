# AWS Supply Chain - Data Generator Deployment
We will be using IaaC (Infraestructure As Code) with AWS Cloud Formation to deploy the solution.
## Pre-requisites
You must have the Lambda functions code as zip (*FOLDER*) in a S3 bucket called "**aws-supply-chain-code-{AccountId}**" and the key must be "data_gen_script.zip" (for the data gen function) and "getS3_objects_script.py.zip" (for the object checker). Also, CloudFormation must have the correct IAM role.

### 1. AWS CloudFormation IAM Role
You have to create the correct role for CloudFormation to perform the operations when creating your stack

AWS CLI 
```bash
aws iam create-role \
    --role-name CfRole \
    --assume-role-policy-document ./Cf.json

```


### 2. Lambda functions code in S3
#### AWS Console
1. Sign in into to your AWS account and open the console.
2. Go to the Amazon S3 service.
3. Select "Create Bucket".
4. Choose "aws-supply-chain-code-{AccountId}" as bucket name (replace AccountID with your account id for your bucket to be unique) and leave the other options as default.
5. Click Next.
6. Download the two zip files from https://gitlab.aws.dev/cjdrago/aws_sc/-/tree/main/awssupplychain_samples-main/zip%20lambdas?ref_type=heads and place them into the bucket you just created.
#### AWS CLI
Copy the following lines into your terminal. You must be connected to Amazon VPN and have "**awscli**" installed
```bash
git clone git@ssh.gitlab.aws.dev:cjdrago/aws_sc.git
cd  ~/aws_sc/awssupplychain_samples-main/zip_lambdas 

# Replace AccountId with your account id
aws s3 create-bucket --bucket aws-supply-chain-code-{AccountId} --region us-east-1
aws s3 cp ~/aws_sc/awssupplychain_samples-main/zip_lambdas s3://aws-supply-chain-code-{AccountId}/ --recursive
```

# Deployment 

### Frontend
To deploy the frontend of the solution, we will be running it locally. 

Pre-requisites: npm installed 
1. Clone client into your PC
```bash
git clone git@ssh.gitlab.aws.dev:cjdrago/aws_sc.git
cd  ~/aws_sc/client 
npm i
npm run dev
```
### Backend
To deploy the backend of the solution, we will be using IaaC with AWS ClouFormation templates.

1. Download the aws_sc_template.json from the /IaaC folder available in this repo.
2. Sign in into your AWS account and open the console.
3. Open the AWS CloudFormation Template
4. Select "Create Stack" -> "With new resources"
4. Select "Template is ready" and "Upload a template file"
5. Upload the **aws_sc_template.json**
7. Click Next
8. In IAM role, select CfRole, click next until its deploying.
6. Wait until it says "CREATION_COMPLETE"
7. Generate your Data!

