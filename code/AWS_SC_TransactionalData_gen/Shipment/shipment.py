# Step 5: Creation of Shipment Records

# Use Inbound Order Line, Inbound Order Line Schedule Records

# Combine df for InboundOrderLineSchedule, InboundOrderLine using id

import numpy as np
import pandas as pd

def set_shipment_delivery_date(shipment_df, days_delta = 7):
    shipment_df['actual_delivery_date'] = shipment_df['planned_delivery_date'] + pd.Timedelta(days = days_delta)


def set_units_shipped(shipment_df):
    shipment_df['units_shipped'] = shipment_df['quantity_confirmed_y'] -  np.random.randint(1, 3, size=1)
    shipment_df['units_shipped'] = shipment_df['units_shipped'].abs()

def shipment_delivery_var(shipment_df, min_delay = 0, max_delay = 30):
    
    for order in shipment_df.order_id.unique():
        order_products_amount = shipment_df.loc[shipment_df.order_id == order, 'actual_delivery_date'].count()
        order_delay = np.random.randint(min_delay, max_delay)
        shipment_df.loc[shipment_df.order_id == order, 'actual_delivery_date'] +=  np.array([order_delay for _ in range(order_products_amount) ], dtype='timedelta64[D]')

def set_shipment_df(inboundOrderLineSchedule_df, InboundOrderLine_df, params):
    shipmentWIP_df = pd.merge(inboundOrderLineSchedule_df,
                           InboundOrderLine_df, on='id', how='inner')
    shipment_df = pd.merge(shipmentWIP_df, params['vendorMatrix'], on='tpartner_id', how='inner')

    drop_columns = ['product_id_x', 'company_id_x', 'order_id_x', 'external_line_number_x', 'quantity_submitted_x', 'schedule_creation_date', 'delivery_date', 'quantity_confirmed_x', 'quantity_received_x','line_creation_date', 'expected_delivery_date_x', 'external_line_number_y', 'quantity_submitted_y', 'quantity_confirmed_y', 'quantity_received_y', 'order_receive_date', 'line_creation_date']

    rename_dict = {'tpartner_id': 'supplier_tpartner_id',
                             'product_id_y': 'product_id',
                             'company_id_y': 'company_id',
                             'order_id_y': 'order_id',
                             'order_line_id_y': 'order_line_id',
                             'to_site_id': 'ship_to_site_id',
                             'expected_delivery_date_y': 'planned_delivery_date'
                             }

    shipment_df.rename(columns = rename_dict, inplace=True)
    set_units_shipped(shipment_df)

    set_shipment_delivery_date(shipment_df)
    shipment_df['package_id'] = 'SCN_RESERVED_NO_VALUE_PROVIDED'
    shipment_df['transportation_mode'] = 'LTL'
    shipment_df['shipment_status'] = 'OPEN'
    shipment_df['carrier_id'] = 'CARR-001'
    shipment_df['uom'] = 'EACHES'
    shipment_df['creation_date'] = shipment_df['line_creation_date']

    
    set_units_shipped(shipment_df)
    shipment_df.drop(columns=drop_columns, inplace=True)
    shipment_delivery_var(shipment_df)
                    
    return shipment_df