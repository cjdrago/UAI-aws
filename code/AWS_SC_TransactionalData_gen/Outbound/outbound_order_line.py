import uuid
import numpy as np
import pandas as pd


def set_outbound_qtty_requested(outbound_df):
    records = outbound_df.shape[0]
    outbound_df['final_quantity_requested'] = np.absolute(np.random.normal(2, 2.75, records).round(decimals=0))


def set_outboundOrderLine_df(data, params, columns_df = ('tpartner_id','product_id', 'company_id', 'ship_from_site_id', 'Xrequested_delivery_date')):
    OutboundOrderLine_df = pd.DataFrame(data, columns = columns_df)
    OutboundOrderLine_df = pd.merge(OutboundOrderLine_df, params['vendorMatrix'], on='tpartner_id', how='inner')
    set_outbound_qtty_requested(OutboundOrderLine_df)

    #Convert to ISO8601Format
    date_columns = ['requested_delivery_date', 'order_date', 'actual_delivery_date', 'promised_delivery_date']
    for date_col in date_columns:
        OutboundOrderLine_df[date_col] = OutboundOrderLine_df['Xrequested_delivery_date'].map(lambda x: x.isoformat())


    OutboundOrderLine_df['status'] = 'OPEN'
    OutboundOrderLine_df['id'] = ["OO_" + str(uuid.uuid1()) for _ in range(len(OutboundOrderLine_df))]
    OutboundOrderLine_df['cust_order_id'] =  ["coid_" + str(uuid.uuid1()) for _ in range(len(OutboundOrderLine_df))]

    
    OutboundOrderLine_df.rename(columns = {'supplier_description':'customer_tpartner_id'}, inplace = True)
    OutboundOrderLine_df = OutboundOrderLine_df.drop(columns = ['Xrequested_delivery_date', 'tpartner_id'], axis=1)


    return OutboundOrderLine_df