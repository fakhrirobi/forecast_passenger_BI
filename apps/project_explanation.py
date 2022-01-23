from dash import html, Input,Output,State,dcc
import dash_bootstrap_components as dbc 


md_docs = ''' 
#####   PROJECT EXPLANATION 


This project used Airport passenger of San Fransisco Airport from 2005 to 2016
 
[Click here to get the Dataset](https://www.kaggle.com/san-francisco/sf-air-traffic-passenger-and-landings-statistics/)
 
This Project was created to aim these following objectives : 

- Create **Time Series Model** for Forecasting Purpose.
- Create **Business Intelligence Dashboard** .
- Create **[API](https://flightpassangerforecast.herokuapp.com/docs)** for forecasting number of passenger of given period
    
##### PROJECT WORKFLOW 

1. Data Cleaning (notebook : )
2. Data Exploration 
3. Creating Forecast Model 
4. Model Evaluation 
5. Creating Dashboard
6. Creating API
7. Deploy both on heroku 

#### Package / Tech Stack Used  
- Dashboard Development : 
    1. Dash 
    2. Dash Bootstrap Component 
    3. Dash Extention 
    4. Plotly 
- Time Series Model Development 
    1. statsmodels
    2. Pandas 
    3. Numpy
- API Development : 
    1. FastAPI
- Deployment : 
    1. Heroku 
    
#### FUTURE PLANS 
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


#### INSTALLATION 

#### Modelling Result 




#### ODDS 
Dashboard Development : 
    1. Dash Syntax is challenging, since its require callback compared to streamlit which only needs like storing as variable to update value 











'''





def render_project_explanation() : 
    content = dcc.Markdown(md_docs)
    content = dbc.Container(
        children = [
            html.Br(), 
            dbc.Row(className='dashboard_picture',
                children = [html.Img(src='https://raw.githubusercontent.com/fakhrirobi/forecast_passenger_BI/main/assets/path-digital-tR0jvlsmCuQ-unsplash.jpg',alt='Dashboard Picture', 
                         style={

                             'height':700,
                               "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto"
                         })]),
        html.Br(),
        dcc.Markdown(md_docs)
            
        
        ])
    
    return content


'''
| No       | Model | MAPE |
| ----------- | ----------- |-----------  |
| 1      | Exponential Smoothing Base Model        | 0.0008154384896421845 |
| 2   | ARIMA p,d,q (1,0,1)   ts_log_diff     | 1.521088082512651 | 
| 3   | ARIMA p,d,q (1,0,1) ts_moving_avg_diff       | 1.521088082512651 |
| 4   | ARIMA p,d,q (1,0,1) ts_log_moving_avg_diff      | 4.003097132106808 |
| 5  | ARIMA p,d,q (1,0,1) moving_avg_sqrt     | 0.0022336601438086657 |
'''


'''
| No       | Model | MAPE |
| ----------- | ----------- |-----------  |
| 1      | RandomForestRegressor       | 0.02821705982449663 |
| 2   | CastBoostRegressor   | 0.06058001839160664 | 
| 3   | XGBoost        | 0.03835722560008849 |
| 4   | Linear Regression     | 0.08068713742097987 |

'''


'''
| No       | Model | MAPE |
| ----------- | ----------- |-----------  |
| 1      | NeuralProphet Base Model 1000 epochs       | 0.015608695722430762 |


'''

