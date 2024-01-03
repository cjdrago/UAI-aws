import os
from Network.site import set_site_records
from Network.transportation_lane import set_transportation_lane
from Organization.company import set_company_records
from Organization.geography import set_geo_records
from Organization.trading_partner import set_tpartner_records
from Planning.inv_policy import set_inv_policy
from Product.product_hierarchy import set_product_hierarchy_records
from Product.products import set_products_records
from Vendor_mgnt.vendor_lead_time import set_vendor_lead_time
from Vendor_mgnt.vendor_product import set_vendor_product
from helpers import load_data, set_partition

def locations_data_gen(country, locations, partition):
    
    sites = []
    for location_json in locations:
        if location_json["main"]:
            set_company_records(location_json, partition) #Set main location as company 
            set_geo_records(country, location_json["country_code"], partition) #Set geography  
        elif location_json["tpartner"]:
            set_tpartner_records(location_json, partition) #Set tpartner location as TradingPartner
        else:
            sites.append(location_json) # Set the other locations as company sites

    set_site_records(sites, partition)

    return sites


def products_data_gen(products, partition):
    
    set_product_hierarchy_records(products, partition)
    set_products_records(products, partition)
    set_vendor_product(products, partition)
    set_inv_policy(products, partition)

def set_responese(event, sites):
    resp = {}

    products = [product_json["id"] for product_json in event["body"]["products"]]
    sites = [site_json["id"] for site_json in sites]

    resp["products"] = products
    resp["sites"] = sites
    resp["datetime"] = event["body"]["datetime"]
    resp["country"] = event["body"]["country"]
    resp["industry"] = event["body"]["industry"]

    return resp

def lambda_handler(event, context):

    country, locations_arr, products_arr, date_time, industry = event["body"]["country"], event["body"]["locations"], event["body"]["products"], event["body"]["datetime"], event["body"]["industry"]

    partition =  'country='+country + '/industry=' + industry + '/' + date_time +'/' 

    sites = locations_data_gen(country, locations_arr, partition)
    GEO = sites[0]["country_code"]

    products_data_gen(products_arr, partition)
    set_transportation_lane(sites, products_arr, partition)
    set_vendor_lead_time(GEO, products_arr, partition)


    resp = set_responese(event, sites)
    return {
        'statusCode': 200,
        'body': resp
    }


if __name__ == "__main__":
    event = load_data()
    lambda_handler(event, "")