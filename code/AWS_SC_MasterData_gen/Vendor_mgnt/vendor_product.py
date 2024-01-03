import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_vendor_product(products_arr, partition):
    
    columns = ["vendor_tpartner_id", "eff_start_date", "eff_end_date", "company_id", "product_id", "vendor_product_code", "vendor_product_desc", "vendor_cost", "vendor_cost_uom", "status", "unit_volume", "volume_uom", "unit_weight", "weight_uom", "release_date", "end_date", "min_order_unit", "country_of_origin", "db_creation_dttm", "db_updation_dttm", "sap_eina__infnr", "sap_eine__ebeln", "sap_eine__ebelp"] 
    data = []
    for product_json in products_arr:
        data_row = [1, "1900-01-01T00:00:00Z", "9999-12-31T00:00:00Z", COMPANY_NAME, product_json["id"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        data.append(data_row)

    VendorProduct_Records = pd.DataFrame(data, columns=columns)

    # save_as_csv(VendorProduct_Records, get_variable_name(VendorProduct_Records=VendorProduct_Records))
    csv_into_s3(partition, VendorProduct_Records, get_variable_name(VendorProduct_Records=VendorProduct_Records)+'.csv')

