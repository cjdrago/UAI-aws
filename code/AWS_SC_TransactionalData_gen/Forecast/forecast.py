import numpy as np
import pandas as pd


def set_forecast_mean(forecast_df):
    recordCounter = forecast_df.shape[0]

    #Generate demand values for these intersections: mean 2, std 2.75 and recordCounter samples
    for z in range (1,recordCounter):
        forecast_df['mean'] = np.random.normal(2, 2.75, recordCounter)

    forecast_df['mean'] = forecast_df['mean'].round(decimals=0)
    forecast_df['mean'] = forecast_df['mean'].abs()   


def set_forecast_df(data, columns = ('product_id', 'site_id','company_id','region_id','product_group_id','snapshot_date')):
    #Create dataframe with all the fixed values list, timestamp, productid
    forecasts_df = pd.DataFrame(data, columns = columns)  
    forecasts_df['forecast_start_dttm'] = forecasts_df['snapshot_date']
    forecasts_df['forecast_end_dttm'] = forecasts_df['snapshot_date']

    set_forecast_mean(forecasts_df)
    
    return forecasts_df