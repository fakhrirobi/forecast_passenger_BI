import pandas as pd 
import numpy as np 
import pandas as pd 
import numpy as np 

import plotly.express as px 

import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt



# // TODO : Use decimal formating 

# DATA_PATH = 'timeseries_data/dataset/pnbp_pernikahan.csv'


# def process_data(data=DATA_PATH) : 
#     data = pd.read_csv(DATA_PATH)  
#     data.loc[:,'Tanggal Penerimaan'] = pd.to_datetime(data.loc[:,'Tanggal Penerimaan'])
#     data= data.groupby('Tanggal Penerimaan').agg({'Nilai' : 'sum'})
#     data = data.reset_index()
#     return data 

def transform_dataset(data) : 
    # Transformation - log ts
    data['log'] = data['Passenger Total'].apply(lambda x: np.log(x))

    # Transformation - 7-day moving averages of log ts
    data['log_moving_avg'] = data['log'].rolling(window = 3,
                                                                center = False).mean()

    # Transformation - 7-day moving average ts
    data['moving_avg'] = data['Passenger Total'].rolling(window = 7,
                                                        center = False).mean()

    # Transformation - Difference between logged ts and first-order difference logged ts
    # data['ts_log_diff'] = data['ts_log'] - data['ts_log'].shift()
    data['log_diff'] = data['log'].diff()

    # Transformation - Difference between ts and moving average ts
    data['moving_avg_diff'] = data['Passenger Total'] - data['moving_avg']

    # Transformation - Difference between logged ts and logged moving average ts
    data['log_moving_avg_diff'] = data['log'] - data['log_moving_avg']

    # Transformation - Difference between logged ts and logged moving average ts
    data = data.dropna()

    # Transformation - Logged exponentially weighted moving averages (EWMA) ts
    data['log_ewma'] = data['log'].ewm(halflife = 7,
                                                                            ignore_na = False,
                                                                            min_periods = 0,
                                                                            adjust = True).mean()

    # Transformation - Difference between logged ts and logged EWMA ts
    data['log_ewma_diff'] = data['log'] - data['log_ewma']
    return data 


# DATA = process_data()

