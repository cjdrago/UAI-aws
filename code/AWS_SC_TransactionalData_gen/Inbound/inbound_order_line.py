import itertools
import uuid
import numpy as np
import pandas as pd


def set_inboundOrderLine_data(params, dateSet):
    '''
        Order Inbound order line data is the product of params values
    '''
    order_line_pool_params = ["partner_id", "product_list", "company", "order_type", "sales_location"]
    order_line_params_values = list(map(params.get, order_line_pool_params))
    order_line_params_values.append(dateSet)
    order_line_data = list(itertools.product(*order_line_params_values))
    return order_line_data

def set_inboundOrderLine_df(data, columns_df = ('tpartner_id','product_id', 'company_id','order_type','to_site_id', 'line_creation_date')):
    InboundOrderLine_df = pd.DataFrame(data, columns = columns_df)

    '''
        El TableKey se hace para agrupar por ordenes (id de la orden):
        e.g.:
            Order_1 involucra envios de multiples productos hacia una localidad especifica
            En total son 520 ordenes. 
            Esto es basicamente el envio especifico de un cargamento con las descripciones de ahi
    ''' 

    InboundOrderLine_df['TableKey'] = InboundOrderLine_df['to_site_id'] + InboundOrderLine_df['line_creation_date'].astype(str) + InboundOrderLine_df['tpartner_id'].astype(str)
    InboundOrderLine_df['order_id'] =   InboundOrderLine_df.TableKey.factorize()[0]+1
    InboundOrderLine_df = InboundOrderLine_df.drop('TableKey', axis=1)
    InboundOrderLine_df['order_id'] = 'Order_' + InboundOrderLine_df['order_id'].astype(str)
    InboundOrderLine_df['id'] = ["OLS_" + str(uuid.uuid1()) for _ in range(len(InboundOrderLine_df))]
    InboundOrderLine_df['external_line_number'] = np.arange(InboundOrderLine_df.shape[0]) + 1

    # Define delta days for expected delivery date. Now it is equal to 10 days
    InboundOrderLine_df['expected_delivery_date'] = InboundOrderLine_df['line_creation_date'] + pd.Timedelta(days=10)
    InboundOrderLine_df['order_receive_date'] = InboundOrderLine_df['line_creation_date'] 

    return InboundOrderLine_df


def set_qtty_InboundOrderLine(InboundOrderLine_df):
    '''
        Set quantitty submitted, confirmed, and recieved
    '''
    records = InboundOrderLine_df.shape[0]

    # I THINK: this entity represents stock transfer between Company locations, not purchases 

    for _ in range (1,records):
        # Quantity submitted is a normal distribution number
        ''' 
            Define Mean and Std from a real case scenario. 
            - Why mean = 3?
            - Why std = 5.75?

            I can work here defining the mean and std from a more technical point
        '''
        
        InboundOrderLine_df['quantity_submitted'] = np.random.normal(3, 5.75, records)
    InboundOrderLine_df['quantity_confirmed'] = InboundOrderLine_df['quantity_submitted']

    # I allways recieve less than what i order
    InboundOrderLine_df['quantity_received'] = (InboundOrderLine_df['quantity_submitted'] - np.random.randint(1,3,size=1)).abs().round(decimals=0)
    InboundOrderLine_df['quantity_submitted'] = InboundOrderLine_df['quantity_submitted'].round(decimals=0).abs()
    InboundOrderLine_df['quantity_confirmed'] = InboundOrderLine_df['quantity_confirmed'].round(decimals=0).abs()

    return InboundOrderLine_df