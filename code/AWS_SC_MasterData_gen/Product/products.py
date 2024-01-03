import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_products_records(products, partition):
    columns = ["id","description","company_id","product_group_id","hts_code","is_hazmat","is_flammable","is_special_handling","is_perishable","is_digital","is_deleted","is_lot_controlled","is_expiry_controlled","creation_date","brand_name","parent_product_id","display_desc","discontinue_day","base_uom","unit_price","currency_uom","product_available_day","shipping_weight","shipping_dimension","unit_volume","pkg_length","pkg_width","pkg_height","weight_uom","dim_uom","volume_uom","casepack_size","gtin","db_creation_dttm","db_updation_dttm","sap_0material_attr__prdha"]
    rows = []

    for product_json in products:
        group_id = product_json["category"] + "_" +  product_json["id"]
        product_row = [product_json["id"], product_json["description"], COMPANY_NAME, group_id, "", "", "", "", "", "", "FALSE", "", "", "", product_json["company"], "", product_json["description"], "", product_json["unit"], product_json["price"], product_json["currency"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        rows.append(product_row)

    Products_Records = pd.DataFrame(rows, columns=columns)

    # save_as_csv(Products_Records, get_variable_name(Products_Records=Products_Records))
    csv_into_s3(partition, Products_Records, get_variable_name(Products_Records=Products_Records)+'.csv')

    