import itertools
import pandas as pd


def set_data(params, params_pool, dateSet = None):
    '''
        Order Inbound order line data is the product of params values
    '''
    order_line_params_values = list(map(params.get, params_pool))
    if dateSet is not None:
        order_line_params_values.append(dateSet)
    order_line_data = list(itertools.product(*order_line_params_values))
    return order_line_data


def create_dateSet(dates_dict, periods = None):
    begin_date, end_date = dates_dict.values()
    dateSet = pd.date_range(start=begin_date, end=end_date, periods=periods)

    return dateSet