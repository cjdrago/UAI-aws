from Forecast.forecast import set_forecast_df
from data_helpers import create_dateSet, set_data
from dates import get_outbound_dates


def gen_forecast(params, t_date):
    '''OJO QUE ESTOY USANDO OUTBOUND DATES Y NO FORECAST DATES'''

    forecast_dates = get_outbound_dates(t_date)
    
    forecast_dateSet = create_dateSet(forecast_dates)
    forecast_params_pool = ["product_list", "sales_location", "company", "region", "product_group"] 
    forecast_data = set_data(params, forecast_params_pool, forecast_dateSet)

    Forecast_Records = set_forecast_df(forecast_data)

    return Forecast_Records