import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_tpartner_records(tpartner_location_json, partition):
    columns = ["id","tpartner_type","geo_id","eff_start_date","eff_end_date","description","company_id","is_active","address_1","address_2","address_3","city","state_prov","postal_code","country","phone_number","time_zone","latitude","longitude","db_creation_dttm","db_updation_dttm"]
    
    row = [[1, "VENDOR", "SCN_RESERVED_NO_VALUE_PROVIDED", "1900-01-01T00:00:00Z", "2050-12-31T23:59:59Z", "Mark LLC", COMPANY_NAME, "TRUE",  tpartner_location_json["address"], "", "", tpartner_location_json["city"], tpartner_location_json["state_prov"], tpartner_location_json["postal_code"], tpartner_location_json["country_code"], tpartner_location_json["phone_number"], tpartner_location_json["time_zone"], tpartner_location_json["latitude"], tpartner_location_json["longitude"], "", ""]]

    TradingPartner_Records = pd.DataFrame(row, columns=columns)
    
    # save_as_csv(TradingPartner_Records, get_variable_name(TradingPartner_Records=TradingPartner_Records))
    csv_into_s3(partition, TradingPartner_Records, get_variable_name(TradingPartner_Records=TradingPartner_Records)+'.csv')

    