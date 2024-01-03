import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv

def set_inv_policy(products, partition):
    columns = ["id","site_id","product_id","product_group_id","dest_geo_id","vendor_tpartner_id","eff_start_date","eff_end_date","company_id","ss_policy","fallback_policy_1","repl_interval","min_safety_stock","max_safety_stock","woc_limit","permitted_var","min_sl","max_sl","db_creation_dttm","db_updation_dttm"]

    data = []

    for product_json in products:
        for site_policy_json in product_json["policies"]:
            inv_policy_id = "InventoryPolicy_" + product_json["id"] + "_" + site_policy_json["location_id"]
            product_group_id = product_json["category"] + \
                "_" + product_json["id"]

            data_row = [
                inv_policy_id,
                site_policy_json["location_id"],
                product_json["id"],
                product_group_id,
                "SCN_RESERVED_NO_VALUE_PROVIDED",
                1,
                "2000-12-19T20:30:22Z",
                "2092-12-19T20:30:22Z",
                COMPANY_NAME,
                "Abs_level",
                "", "",
                site_policy_json["min_safety_stock"],
                site_policy_json["max_safety_stock"],
                "", "", "", "", "", ""
            ]

            data.append(data_row)

    InventoryPolicy_Records = pd.DataFrame(data, columns=columns)
    
    # save_as_csv(InventoryPolicy_Records, get_variable_name(InventoryPolicy_Records=InventoryPolicy_Records))
    csv_into_s3(partition, InventoryPolicy_Records, get_variable_name(InventoryPolicy_Records=InventoryPolicy_Records)+'.csv')

    