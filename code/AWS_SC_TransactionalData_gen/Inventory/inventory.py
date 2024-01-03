import numpy as np
import pandas as pd
from data_helpers import set_data


def set_inventory_df(params, t_date):

    inv_params_pool = ['product_list','company','sales_location']
    inventory_data = set_data(params, inv_params_pool)
    InventoryLevel_df = pd.DataFrame(inventory_data, columns = ('product_id', 'company_id','site_id'))
    InventoryLevel_df['snapshot_date'] = pd.Timestamp(t_date)

    set_inventory_amount(InventoryLevel_df, InventoryLevel_df.shape[0])

    InventoryLevel_df['inv_condition'] = 'SCN_RESERVED_NO_VALUE_PROVIDED'

    InventoryLevel_df['lot_number'] = 'SCN_RESERVED_NO_VALUE_PROVIDED'

    return InventoryLevel_df


def set_inventory_amount(inventory_level_df, records):

    '''
        On hand inventory is a random number between 2 and 60
    '''
    inventory_level_df['on_hand_inventory'] = pd.DataFrame(np.random.randint(2,60,size=records))
    inventory_level_df['allocated_inventory'] = (inventory_level_df['on_hand_inventory'] - np.random.randint(2,15,size=records)).round(decimals=0).abs()
    

    pass
