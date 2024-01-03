#Step 8: Creation of Outbound Shipment Records
import uuid


def set_OutboundShipment_df(OutboundShipment_df):

    OutboundShipment_df['cust_order_line_id'] = [
        "colid_" + str(uuid.uuid1()) for _ in range(len(OutboundShipment_df))]
    rename_cols_dict = {'final_quantity_requested': 'shipped_qty',
                         'requested_delivery_date': 'expected_ship_date',
                         'order_date': 'actual_ship_date',
                         'actual_delivery_date': 'actual_delivery_date',
                         'promised_delivery_date': 'db_creation_dttm',
                         'ship_from_site_id': 'from_site_id'
                         }
    
    drop_cols = ['customer_tpartner_id', 'status']
    
    OutboundShipment_df.rename(columns = rename_cols_dict, inplace = True)
    OutboundShipment_df = OutboundShipment_df.drop(columns = drop_cols, axis=1)

    return OutboundShipment_df