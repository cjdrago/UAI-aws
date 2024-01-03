import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_site_records(locations_arr, partition):
    

    columns = ["id","description","company_id","geo_id","address_1","address_2","address_3","city","state_prov","postal_code","country","phone_number","time_zone","site_type","unlocode","latitude","longitude","is_active","open_date","end_date","db_creation_dttm","db_updation_dttm"]
    rows = []

    for location_json in locations_arr:
        
        #Warehouse -> ???
        row = [location_json["id"], location_json["city"] + ", " + location_json["country_code"], COMPANY_NAME, location_json["country_code"],location_json["address"], "", "", location_json["city"], location_json["state_prov"], location_json["postal_code"], location_json["country_code"], location_json["phone_number"], location_json["time_zone"], "Warehouse", "", location_json["latitude"], location_json["longitude"], "TRUE", "", "", "", ""]
        rows.append(row)
    
    Site_Records = pd.DataFrame(rows, columns=columns)
    
    # save_as_csv(Site_Records, get_variable_name(Site_Records=Site_Records))
    csv_into_s3(partition, Site_Records, get_variable_name(Site_Records=Site_Records)+'.csv')

    