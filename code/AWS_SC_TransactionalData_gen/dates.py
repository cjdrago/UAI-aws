import pandas as pd

def get_today_date():
    tdate = pd.Timestamp("today", tz='America/Santiago')
    return tdate

def get_forecasts_date(tdate, forward_delta = 72):
    f_dates = {
        'begin_date' : tdate,
        'end_date' : tdate + pd.Timedelta(days=forward_delta)
    }

    return f_dates

def get_full_dates(tdate, forward_delta=72, backwards_delta=1000):
    full_dates = {
        "begin_date": tdate - pd.Timedelta(days=backwards_delta),
        "end_date" : tdate + pd.Timedelta(days=forward_delta)
        }
    
    return full_dates


def get_outbound_dates(tdate, h_delta = 72):
    h_dates = {
        "begin_date" : tdate - pd.Timedelta(days = h_delta),
        "end_date" : tdate + pd.Timedelta(days = h_delta)
    }
    return h_dates

if __name__ == "__main__":
    print(get_today_date())