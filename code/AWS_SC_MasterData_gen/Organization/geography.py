

import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_geo_records(country, country_code, partition):
    columns = ["id","description","company_id","parent_geo_id","address_1","address_2","address_3","city","state_prov","postal_code","country","phone_number","time_zone","db_creation_dttm","db_updation_dttm"]
    row = [country_code, country, COMPANY_NAME, "", "", "", "", "", "", "", country_code, "", "", "", ""]
    Geography_Records = pd.DataFrame([row], columns=columns)   

    #Instead of saving csv, we have to save it in S3
    # save_as_csv(Geography_Records, get_variable_name(Geography_Records=Geography_Records))
    csv_into_s3(partition, Geography_Records, get_variable_name(Geography_Records=Geography_Records)+'.csv')
