import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv


def set_vendor_lead_time(GEO, products, partition):
    columns = ["vendor_tpartner_id", "product_id", "product_group_id", "site_id", "region_id", "eff_start_date", "eff_end_date", "company_id", "planned_lead_time", "planned_lead_time_dev",
               "actual_lead_time_mean", "actual_lead_time_sd", "actual_p50", "actual_p90", "shipping_cost", "cost_uom", "we_pay", "db_creation_dttm", "db_updation_dttm", "sap_eina__infnr"]
    data = []

    for product_json in products:
        for site_policy_json in product_json["policies"]:
            product_group_id = product_json["category"] + \
                "_" + product_json["id"]
            data_row = [
                1,
                product_json["id"],
                product_group_id,
                site_policy_json["location_id"],
                GEO,
                "1900-01-01T00:00:00Z",
                "9999-12-31T00:00:00Z",
                COMPANY_NAME,
                site_policy_json["planned_lead_time"],
                site_policy_json["planned_lead_time_dev"],
                site_policy_json["planned_lead_time_mean"],
                "", "", "", "", "", "", "", "", ""
            ]

            data.append(data_row)

    VendorLeadTime_Records = pd.DataFrame(data, columns=columns)
    # save_as_csv(VendorLeadTime_Records, get_variable_name(VendorLeadTime_Records=VendorLeadTime_Records))
    csv_into_s3(partition, VendorLeadTime_Records, get_variable_name(VendorLeadTime_Records=VendorLeadTime_Records)+'.csv')


