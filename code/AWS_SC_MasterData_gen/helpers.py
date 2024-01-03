from io import StringIO
import os
import json
import pandas as pd
import boto3

s3 = boto3.client('s3')
sts = boto3.client('sts')

COMPANY_NAME = "ACPG"
PARTITION = ""

def set_partition(partition):
    PARTITION = partition

def get_variable_name(**variables):
    return [x for x in variables][0]

def save_as_csv(data, name):
    data.to_csv(name+'.csv', index=False, date_format='%Y-%m-%dT%H:%M:%SZ') 

def csv_into_s3(partitions, data_df, file_name, bucket = "aws-sc-data"):
    
    AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]
    csv_buffer = StringIO()
    data_df.to_csv(csv_buffer)
    s3.put_object(
        Bucket = bucket+'-'+AWS_ACCOUNT_ID,
        Key = partitions + file_name,
        Body = csv_buffer.getvalue()
    )


def create_master_data_folder(path):
    os.chdir(path)
    folder_name = "Master_Data"
    if folder_name not in os.listdir():
        os.mkdir(folder_name)
        
    os.chdir(folder_name)

def load_data(file_name = "test-payload.json"):
    file = open(file_name)
    data_json = json.load(file)
    return data_json