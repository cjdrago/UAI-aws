from Shipment.shipment import set_shipment_df, shipment_delivery_var


def gen_shipment(InboundOrderLineSchedule_Records_copy, InboundOrderLine_Records_copy, params):
    Shipment_Records = set_shipment_df(InboundOrderLineSchedule_Records_copy, InboundOrderLine_Records_copy, params)
    shipment_delivery_var(Shipment_Records)

    return Shipment_Records