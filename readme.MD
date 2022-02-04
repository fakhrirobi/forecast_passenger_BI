


### :bar_chart: CREATING AIR FLIGHT PASSENGER BUSINESS INTELLIGENCE DASHBOARD
#####  :pencil2:  PROJECT EXPLANATION 
---


This project used Airport passenger of San Fransisco Airport from 2005 to 2016
 
[Click here to get the Dataset](https://www.kaggle.com/san-francisco/sf-air-traffic-passenger-and-landings-statistics/)
 
This Project was created to aim these following objectives : 

- Create **[Time Series Model](https://github.com/fakhrirobi/airtraffic_forecast)** for Forecasting Purpose.
- Create **[Business Intelligence Dashboard](https://github.com/fakhrirobi/forecast_passenger_BI)** .
- Create **[API](https://flightpassangerforecast.herokuapp.com/docs)** for forecasting number of passenger of given period
    
##### :pencil2: PROJECT WORKFLOW 
---
1. Dataset Exploration 
2. Chart Exploration 
3. Dashboard Layouting 
4. Creating Dashboard
5. Deploy both on heroku 

#### :wrench: Package / Tech Stack Used  
---
- Dashboard Development : 
    1. Dash
    2. Dash Bootstrap Component 
    3. Dash Extention -> for lottie sticker
    4. Plotly -> creating figure 
   
   
   
- Deployment : 
    1. Heroku 
    
#### :hourglass: FUTURE PLANS 
---
- Time Series Model Development 
    1. Use Deep Learning, Supervised ML, 
    2. Pandas 
    3. Numpy
   
- API Development : 
    1. Generate API Key 
    2. Create DB (Using PostgreSQL) for API Key and Request 

- Deployment : 
    1. Deploy on GCP / AWS 
    
- Other Devs : 
    1. Create workflow to fetch API Data with Apache Airflow  
    2. Create Package using Pip  
    3. Use cookiecutter
    4. Implement Testing 


#### :gem: FINAL PRODUCT 

You can access the webapp in : https://dashboardpassenger.herokuapp.com/

Snapshot of the app : 
!['gif gile of the display of the dashboard'](https://github.com/fakhrirobi/forecast_passenger_BI/blob/main/demo/demo.gif)

#### :hammer: INSTALLATION 
---
```python
#clone the repository first 
    git clone https://github.com/fakhrirobi/forecast_passenger_BI.git
```
```python
#change directory 
    cd forecast_passenger_BI
```
```python
#run index.py 
    python index.py 
```
#### :green_book: Modelling Result 

|    |     RMSE Score |       MAE Score |   MAPE Score | model_name                                               |
|---:|---------------:|----------------:|-------------:|:---------------------------------------------------------|
|  1 |    2.9332e+10  | 120793          |  0.028163    | RandomForestRegressor                                    |
|  2 |    3.94132e+10 | 160227          |  0.0383572   | XGBRegressor                                             |
|  3 |    8.33301e+11 | 823894          |  0.195214    | SVRegressor                                              |
|  4 |    1.98349e+11 | 364297          |  0.0889501   | KNeighborsRegressor                                      |
|  5 |    1.51227e+11 | 323093          |  0.0806871   | LinearRegression                                         |
|  6 |    3.45687e+11 | 484491          |  0.11898     | PassiveAggressiveRegressor                               |
|  7 |    4.29552e+09 |  52562.4        |  0.0160444   | NeuralProphet_hidden_layer3_epoch_3_weekly_seasonality12 |
|  8 |    0.00879809  |      0.0750631  |  0.00494308  | SARIMA_1,0,1_1,0,1,12_ts_log                             |
|  9 |    0.000148183 |      0.00870418 |  0.0005716   | SARIMA_1,0,1_1,0,1,12_ts_log_moving_avg                  |
|  10 |    3.51627e+10 | 127422          |  0.0310854   | SARIMA_1,0,1_1,0,1,12_ts_moving_avg                      |
|  11 |    0.000148428 |      0.00895553 |  0.000589953 | SARIMA_1,0,1_1,0,1,12_ts_log_ewma                        |
|  12 |    0.00758013  |      0.0672904  |  0.977108    | SARIMA_1,0,1_1,0,1,12_ts_log_ewma_diff                   |
|  13 | 7724.52        |     69.9086     |  0.0352462   | SARIMA_1,0,1_1,0,1,12_sqrt_ts                            |
|  14 |  308.334       |     10.7121     |  0.00528588  | SARIMA_1,0,1_1,0,1,12_moving_avg_sqrt                    |


..
#### :email: Connect With Me 
---
Dashboard Development : 

 1. Dash Syntax is challenging, since its require callback compared to streamlit which only needs like storing as variable to update value. However dash create more stunning dashboard.  
   
 2. 
   



..

#### Connect With Me 
---
1. [Linkedin](https://www.linkedin.com/in/fakhrirobi/)
2. [Medium](https://www.medium.com/@fakhrirobi.fra/)
3. [Kaggle](https://www.kaggle.com/fakhrirobi/)