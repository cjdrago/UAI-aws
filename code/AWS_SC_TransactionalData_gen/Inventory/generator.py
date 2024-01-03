from Inventory.inventory import set_inventory_df


def gen_inventory(params, t_date):
     InventoryLevel_Records = set_inventory_df(params, t_date)
     return InventoryLevel_Records
    