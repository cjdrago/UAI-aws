# Implementation Guide (us-east-1)
This implementation is based on AWS CloudFormation service, an Infrastructure As Code (IaaC) service. 

YOU MUST BE IN ***US-EAST-1*** REGION

## Step 1 
Copy the zip code into a new s3 bucket in your account.

1. Open the terminal
2. Run the following command:
```bash
sh loadLambdas.sh
```

This will create an S3 bucket named "aws-sc-code-{AWS-AccountID}". Inside this bucket, you will have 4 zip files that contains the code of the project. 
## Step 2
Launch the Cloud Formation template.

#### Create CloudFormation IAM Role
1. In the AWS Console search bar, look for IAM service.
3. In the left panel, select Roles and then Create role.
4. Select AWS Service as Trusted entity type.
5. Look for CloudFormation in the use case, and Click next.
6. Select AdministratorAccess and click next.
7. Choose a name, and click create role.

#### Launch the CloudFormation template
8. In the AWS Console search bar, look for CloudFormation service.
9. Choose Create Stack with new resources.
10. Choose Template is ready option (selected by default).
11. On the Specify template section, select the Upload a template file option.
12. Download the "IaaC-template.json" file from this repo and upload it as template to the AWS Console.
13. Click Next.
14. Enter a Stack Name, and in parameters write the bucket name you created at Step 1 (aws-sc-code-{AWS-AccountID}). Then click Next.
15. On the Permissions section, select the IAM role you created on Step 2.7
16. Click Next, and then Click Submit.
17. Wait until CREATION_COMPLETE is set as status.
18. Now the infrastructure is ready to use.
