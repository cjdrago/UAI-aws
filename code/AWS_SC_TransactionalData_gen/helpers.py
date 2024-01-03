import os
import json
import pandas as pd

def get_variable_name(**variables):
    return [x for x in variables][0]

def save_as_csv(data, name):
    data.to_csv(name+'.csv', index=False, date_format='%Y-%m-%dT%H:%M:%SZ') 

def create_transactional_folder(path):
    os.chdir(path)
    folder_name = "Transactional_Data"
    if folder_name not in os.listdir():
        os.mkdir(folder_name)
        
    os.chdir(folder_name)


def get_params(sites_ids, products_ids):

    f = open("params.json")
    params = json.load(f)

    params["sales_location"] = sites_ids
    params["product_list"] = products_ids

    params["vendorMatrix"] = pd.DataFrame.from_dict(params["vendorMatrix2"])

    return params

def load_data(file_name = "test-payload.json"):
    file = open(file_name)
    data_json = json.load(file)
    return data_json
