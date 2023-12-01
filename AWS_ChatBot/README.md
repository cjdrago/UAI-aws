# AWS Supply Chain - Chatbot
To implement this solution, you must follow the aplication deployment from [AWS Solutions](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws).

Once we deployed the solution we have to add context using an Amazon Kendra conection. We will be using Amazon S3 as a data source Kendra.

### 1. Clone data into S3 Bucket
> Bucket name must be unique, replace **AccountId** with your account ID or a random number.
#### CLI
```bash 
git clone git@ssh.gitlab.aws.dev:cjdrago/aws_sc.git
cd  ~/aws_sc/awssupplychain_samples-main/ContextFiles 

# Replace AccountId with your account id
aws s3 create-bucket --bucket aws-supply-chain-context-{AccountId} --region us-east-1
aws s3 cp ~/aws_sc/awssupplychain_samples-main/ContextFiles s3://aws-supply-chain-context-{AccountId}/ --recursive
```
#### Console

1. Sign in into to your AWS account and open the console.
2. Go to the Amazon S3 service.
3. Select "Create Bucket".
4. Choose "aws-supply-chain-context-{AccountId}" as bucket name (replace AccountID with your account id for your bucket to be unique) and leave the other options as default.
5. Click Next.
6. Download the ContextFiles folder from https://gitlab.aws.dev/cjdrago/aws_sc/-/tree/main/awssupplychain_samples-main/ContextFiles?ref_type=heads and place them into the bucket you just created.

### 2. Create an Amazon Kendra IAM Role
First, open the KendraRole.json file in this repo, and in the lines 22 and 23 replace the **{AccountId}** with your Account Id.

```bash
aws iam create-role \
    --role-name Kendra-Role \
    --assume-role-policy-document ./KendraRole.json

```

This command will output something like this:

```json
{
    "Role": {
        "AssumeRolePolicyDocument": "<URL-encoded-JSON>",
        "RoleId": "XXX",
        "CreateDate": "XXX",
        "RoleName": "Kendra-Role",
        "Path": "/",
        "Arn": "arn:aws:iam::XXXX:role/Kendra-Role"
    }
}
```
Copy and paste the role ARN to use it later.

### 3. Create an Amazon Kendra index
```bash
aws kendra create-index \
    --name "awsScContext" \
    --role-arn '{ROLE ARN}'
```

This command will output the index Id, copy and paste it into another file to use it later.

### 4. Create an Amazon Kendra connection for S3
#### CLI
```bash
aws kendra create-data-source \
 --index-id {INDEX ID} \
 --name aws-sc-context \
 --type S3 \
 --configuration '{"S3Configuration":{"BucketName":"aws-supply-chain-context-{AccountId}"}}' 
 --role-arn '{ROLE ARN}'
```