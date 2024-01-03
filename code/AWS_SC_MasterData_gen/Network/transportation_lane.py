from geopy.distance import geodesic, distance # Distance by latitude and longitude
import numpy as np
import pandas as pd
from helpers import COMPANY_NAME, csv_into_s3, get_variable_name, save_as_csv

def get_distance(from_site_json, to_site_json):
    from_site_coord = (from_site_json["latitude"], from_site_json["longitude"])
    to_site_coord = (to_site_json["latitude"], to_site_json["longitude"])
    
    return int(distance(from_site_coord, to_site_coord).km), "KM"

def transportaion_policy(sites, products):
    products_amount = len(products)
    sites_amount = len(sites)

    # Contains logic of transportation from_site_X to every other site, by product_group_id 
    transportation_policy_dict = {}

    for site_json, site_indx in zip(sites, range(sites_amount)):
        '''
            Random logic of transportation lane for a specific site from the current location, by product_grup
            Examle: 4 locations and 3 products
            from_site_0 = 
                   to_site 0: [[0,0,0],  //cant send any product from site 0 to site 0
                   to_site 1:  [1,0,1],  //can send to site 1 products 0 and 2
                   to_site 2:  [0,1,0],  //can send to site 2 only product 1
                   to_site 3:  [1,1,1]]  //can send to site 3 any product
        '''
        site_transportation_logic_arr = np.random.randint(2, size=(sites_amount, products_amount))
        site_transportation_logic_arr[site_indx][:] = 0
        transportation_policy_dict["from_site_"+site_json["id"]] = site_transportation_logic_arr.tolist()

    return transportation_policy_dict, sites
        
def set_transportation_lane(sites, products, partition):

    columns = ["id","from_site_id","to_site_id","from_geo_id","to_geo_id","carrier_tpartner_id","trans_mode","service_type","product_group_id","company_id","transit_time","time_uom","distance","distance_uom","eff_start_date","eff_end_date","daily_start_time","daily_end_time","open_sun","open_mon","open_tue","open_wed","open_thu","open_fri","open_sat","cost_per_unit","cost_per_weight","cost_currency","weight_uom","emissions_per_unit","emissions_per_weight"]

    transportation_policy_dict, sites = transportaion_policy(sites, products)
    
    data = []
    transportation_lane_id = 0
    to_sites, products_amount = len(sites), len(products)
    GEO =  sites[0]["country_code"]

    # TODO: Improve code -> 3 for statments :(
    for site_transportation_policy, site_json in zip(transportation_policy_dict.values(), sites):
        for site_indx in range(to_sites):
            for product_indx in range(products_amount):

                if site_transportation_policy[site_indx][product_indx] == 1:
                    product_group_id = products[product_indx]["category"] + "_" +  products[product_indx]["id"]
                    distance, distance_uom = get_distance(site_json, sites[site_indx])

                    data_row = ["TransportationLane_"+str(transportation_lane_id),
                                site_json["id"],
                                sites[site_indx]["id"],
                                GEO,
                                GEO,
                                "CARR-001", #WHAT IS THIS???
                                "LTL", #WHAT IS THIS???
                                "SCN_RESERVED_NO_VALUE_PROVIDED",
                                product_group_id,
                                COMPANY_NAME,
                                "TRANSIT TIME",
                                "TIME UOM",
                                distance,
                                distance_uom,
                                "1900-01-01T00:00:00Z",
                                "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
                    transportation_lane_id += 1
                    data.append(data_row)
            
    TransportationLane_Records = pd.DataFrame(data, columns=columns)
    # save_as_csv(TransportationLane_Records, get_variable_name(TransportationLane_Records=TransportationLane_Records))
    csv_into_s3(partition, TransportationLane_Records, get_variable_name(TransportationLane_Records=TransportationLane_Records)+'.csv')

