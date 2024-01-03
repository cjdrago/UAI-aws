
from Inbound.inbound_order import set_InboundOrder_df
from Inbound.inbound_order_line import set_inboundOrderLine_df, set_qtty_InboundOrderLine
from Inbound.inbound_order_line_schedule import set_InboundOrderLineSchedule_df
from data_helpers import create_dateSet, set_data
from dates import get_full_dates


def gen_inbound_order_line(params, t_date, num_periods):
    inboundOrder_dates = get_full_dates(t_date)
    InboundOrder_dateSet = create_dateSet(inboundOrder_dates, num_periods)
    order_line_params_pool = ["partner_id", "product_list", "company", "order_type", "sales_location"]    
    inboundOrderLine_data = set_data(params, order_line_params_pool, InboundOrder_dateSet)
    InboundOrderLine_Records = set_inboundOrderLine_df(inboundOrderLine_data)
    InboundOrderLine_Records = set_qtty_InboundOrderLine(InboundOrderLine_Records)

    return InboundOrderLine_Records

def gen_inbound_order_schedule(InboundOrderLine_df_copy):
    InboundOrderLineSchedule_Records = set_InboundOrderLineSchedule_df(InboundOrderLine_df_copy)

    return InboundOrderLineSchedule_Records


def gen_inbound_order(InboundOrderLine_df_copy):
    InboundOrder_Records = set_InboundOrder_df(InboundOrderLine_df_copy)
    
    return InboundOrder_Records
