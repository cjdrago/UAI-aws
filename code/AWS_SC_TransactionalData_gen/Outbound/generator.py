from Outbound.outbound_order_line import set_outboundOrderLine_df
from Outbound.outbound_shipment import set_OutboundShipment_df
from data_helpers import create_dateSet, set_data
from dates import get_outbound_dates


def gen_outbound_order_line(params, t_date):
    outbound_dates = get_outbound_dates(t_date)
    outbound_dateSet = create_dateSet(outbound_dates)
    outbound_params_pool = ['partner_id', 'product_list','company','sales_location']
    outbound_data = set_data(params, outbound_params_pool, outbound_dateSet)

    OutboundOrderLine_Records = set_outboundOrderLine_df(outbound_data, params) 
    
    return OutboundOrderLine_Records


def gen_outbound_shipment(OutboundOrderLine_copy):
    OutboundShipment_Records = set_OutboundShipment_df(OutboundOrderLine_copy)
    
    return OutboundShipment_Records