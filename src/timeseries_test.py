

#Importing all dependencies 
import plotly.express as px 
import plotly.graph_objects as go 
import pandas as pd 
import plotly.tools as tls 
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf,acf

import matplotlib.pyplot as plt 


from statsmodels.graphics.tsaplots import plot_pacf,plot_acf

# to implement this function i need to write callback function in dash to ease up my job 
def test_stationarity(df, ts):
    """
    Test stationarity using moving average statistics and Dickey-Fuller test
    Source: https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
    
    This function was aimed to test the classical assumption of timeseries data, which consists of : 
    1. No change on mean over time 
    2. No change on variance over time 
    """
    
    # Determing rolling statistics
    rolmean = df[ts].rolling(window = 12, center = False).mean()
    rolstd = df[ts].rolling(window = 12, center = False).std()
    
    # Plot rolling statistics:
    
    fig = go.Figure()
    fig.add_trace(go.Line(
        x=df['Tanggal Penerimaan'], 
        y=df[ts],name='original value'
    ))
    fig.add_trace(go.Line(
        x=df['Tanggal Penerimaan'], 
        y=rolmean,name='rolling mean'
    ))
    fig.add_trace(go.Line(
        x=df['Tanggal Penerimaan'], 
        y=rolstd,name = 'rolling standard deviation'
    ))
    
    fig.update_layout(
        title = f'Rolling Mean and Standard Deviation for {ts}'
    )
    
    # Perform Dickey-Fuller test:
    # Null Hypothesis (H_0): time series is not stationary
    # Alternate Hypothesis (H_1): time series is stationary
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(df[ts], 
                    autolag='AIC')
    
    dfoutput = pd.Series(dftest[0:4], 
                        index = ['Test Statistic',
                                'p-value',
                                '# Lags Used',
                                'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
        
    print('Stationarity Test Result : ')
    
    if dfoutput['p-value'] <= 0.05 : 
            print('The Data Is Stationary')
    else : 
        container.warning('The Data Is Non-Stationary')
    container.dataframe(dfoutput)
    return fig


def plot_acf_pacf(df,ts) : 
    pacf_figure = plot_pacf(df[ts])
    acf_figure = plot_acf(df[ts])
    # // TODO : create subplot to combine both chart 
    fig,(ax1,ax2) = plt.subplots(nrows=2,ncols=1)
    
    
    return pacf_figure,acf_figure 