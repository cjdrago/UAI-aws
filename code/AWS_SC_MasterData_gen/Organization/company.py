import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_company_records(main_location_json, partition):
    columns = ["id","description","address_1","address_2","address_3","city","state_prov","postal_code","country","phone_number","time_zone","db_creation_dttm","db_updation_dttm"]
    row = [COMPANY_NAME, COMPANY_NAME, main_location_json["address"], "", "", main_location_json["city"], main_location_json["state_prov"], main_location_json["postal_code"], main_location_json["country_code"], main_location_json["phone_number"], main_location_json["time_zone"], "", ""]

    Company_Records = pd.DataFrame([row], columns=columns)   

    # save_as_csv(Company_Records, get_variable_name(Company_Records=Company_Records))
    csv_into_s3(partition, Company_Records, get_variable_name(Company_Records=Company_Records)+'.csv')
