import plotly.express as px 
import plotly.graph_objects as go 


import pandas as pd 
import numpy as np 
import joblib 

from statsmodels.tsa.arima_model import ARIMA


MODEL_PATH = 'timeseries_data/model/arima_model.joblib'



def transform_data(df,ts='Nilai') : 
    ''' 
    This function was aimed to handle non stationary data before feeding into arima model 
    
    
    '''
    # Transformation - log ts
    df['ts_log'] = df[ts].apply(lambda x: np.log(x))

    # Transformation - 7-day moving averages of log ts
    df['ts_log_moving_avg'] = df['ts_log'].rolling(window = 7,
                                                                center = False).mean()

    # Transformation - 7-day moving average ts
    df['ts_moving_avg'] = df['Nilai'].rolling(window = 7,
                                                        center = False).mean()

    # Transformation - Difference between logged ts and first-order difference logged ts
    # df_example['ts_log_diff'] = df_example['ts_log'] - df_example['ts_log'].shift()
    df['ts_log_diff'] = df['ts_log'].diff()

    # Transformation - Difference between ts and moving average ts
    df['ts_moving_avg_diff'] = df['Nilai'] - df['ts_moving_avg']

    # Transformation - Difference between logged ts and logged moving average ts
    df['ts_log_moving_avg_diff'] = df['ts_log'] - df['ts_log_moving_avg']

    # Transformation - Difference between logged ts and logged moving average ts
    df = df.fillna(0)

    # Transformation - Logged exponentially weighted moving averages (EWMA) ts
    df['ts_log_ewma'] = df['ts_log'].ewm(halflife = 7,
                                                                        ignore_na = False,
                                                                            min_periods = 0,
                                                                            adjust = True).mean()

    # Transformation - Difference between logged ts and logged EWMA ts
    df['ts_log_ewma_diff'] = df['ts_log'] - df['ts_log_ewma']
    
    # for col in df.columns : 
    #     if col != 'Nilai' : 
    #         test_stationarity(df,col,container=timeseries_test)
    #     else : 
    #         continue
    return df 



def run_arima_model(df, ts, p, d, q,save_model=False):
    """
    Run ARIMA model : 
    Parameters : 
    df -> dataframe 
    ts -> column name of timeseries data 
    p -> 
    d -> 
    q ->
    
    Returns : 
    fit_model -> Trained ARIMA Model object 
    rmse -> RMSE Score 
    figure -> figure object of real vs predicted values 
    """
    

    # fit ARIMA model on time series
    model = ARIMA(df[ts], order=(p, d, q))  
    fit_model = model.fit(disp=-1)  
    
    
    
    # get lengths correct to calculate RSS
    len_results = len(fit_model.fittedvalues)
    ts_modified = df[ts][-len_results:]
    
    # calculate root mean square error (RMSE) and residual sum of squares (RSS)
    rss = sum((fit_model.fittedvalues - ts_modified)**2)
    rmse = np.sqrt(rss / len(df[ts]))
    
    # plot fit
    #plotly chart 
    figure = go.Figure()
    figure.add_trace(go.Line(
        x=df['Tanggal Penerimaan'], 
        y=df[ts],name='Original Values'
    ))
    
    figure.add_trace(go.Line(
        x=df['Tanggal Penerimaan'], 
        y=fit_model.fittedvalues,name='Predicted values'
    ))
    figure.update_layout(title=f'''For ARIMA model with parameter = ({p},{d},{q}) has <br> RSS = {rss:.4f} and RMSE = {rmse:.4f}''')
    if save_model : 
        fit_model.save(MODEL_PATH)

    
    return fit_model,rmse,figure