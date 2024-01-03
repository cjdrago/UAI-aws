def set_InboundOrder_df(InboundOrder):
    
    columns_to_drop = ['product_id', 'line_creation_date', 'to_site_id', 'id','external_line_number', 'quantity_submitted', 'quantity_confirmed', 'quantity_received', 'order_receive_date', 'expected_delivery_date']

    InboundOrder['order_creation_date'] = InboundOrder['line_creation_date'] 

    InboundOrder['submitted_date'] = InboundOrder['line_creation_date'] 

    InboundOrder = InboundOrder.drop(columns_to_drop, axis=1)
    InboundOrder.rename(columns = {'order_id':'id'}, inplace = True)

    InboundOrder.drop_duplicates(subset=['id'], inplace=True)
    return InboundOrder