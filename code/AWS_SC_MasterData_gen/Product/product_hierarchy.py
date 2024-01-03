import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_product_hierarchy_records(products, partition):

    columns = ["id","description","company_id","parent_product_group_id","creation_date","update_date","db_creation_dttm","db_updation_dttm"]
    rows = []
    for product_json in products:
        group_id = product_json["category"] + "_" +  product_json["id"]
        row = [group_id,  product_json["description"], COMPANY_NAME,  product_json["category"], "", "", "", ""]
        rows.append(row)
    ProductHierarchy_Records = pd.DataFrame(rows, columns=columns)
    
    # save_as_csv(ProductHierarchy_Records, get_variable_name(ProductHierarchy_Records=ProductHierarchy_Records))
    csv_into_s3(partition, ProductHierarchy_Records, get_variable_name(ProductHierarchy_Records=ProductHierarchy_Records)+'.csv')
