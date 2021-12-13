from dash import html, Input,Output,State,dcc
import dash_bootstrap_components as dbc 


md_docs = ''' 
#####   PROJECT EXPLANATION 

![Dashboard Picture](https://raw.githubusercontent.com/fakhrirobi/forecast_passenger_BI/main/assets/path-digital-tR0jvlsmCuQ-unsplash.jpg)
This project used Airport passenger of San Fransisco Airport from 2005 to 2016
 
[Click here to get the Dataset](https://www.kaggle.com/san-francisco/sf-air-traffic-passenger-and-landings-statistics/)
 
This Project was created to aim these following objectives : 

- Create **Time Series Model** for Forecasting Purpose.
- Create **Business Intelligence Dashboard** .
    
##### PROJECT WORKFLOW 








'''
def render_project_explanation() : 
    content = dcc.Markdown(md_docs)
    
    return content