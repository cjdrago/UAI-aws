import pandas as pd


def set_InboundOrderLineSchedule_df(InboundOrderLineSchedule):

    columns_to_drop = ["tpartner_id", "line_creation_date", "order_type", "to_site_id", "order_receive_date"]

    # Foreign key 
    InboundOrderLineSchedule['order_line_id'] = InboundOrderLineSchedule['id']

    # Set schedule creation date a the line creation date
    InboundOrderLineSchedule['schedule_creation_date'] = InboundOrderLineSchedule['line_creation_date']

    # Delivery date is not the expected one, 7 days more
    InboundOrderLineSchedule['delivery_date'] = InboundOrderLineSchedule['expected_delivery_date'] + pd.Timedelta(days=7)

    InboundOrderLineSchedule = InboundOrderLineSchedule.drop(columns_to_drop, axis=1)


    return InboundOrderLineSchedule