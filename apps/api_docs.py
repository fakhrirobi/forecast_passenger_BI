from dash import html, Input,Output,State,dcc
import dash_bootstrap_components as dbc 

markdown_embed = ''' 
```python 
pip install dash




'''
paragraph = '''

You can use this API by this following ways : 

1. python (using request)
2. postman 
3. etc 

#### API Link 

https://flightpassangerforecast.herokuapp.com/forecast_timeseries

---
#### Request Body 

  "month_limit": "string" 
    date format : "YYYY-MM-01" 
    forecast is montly based , minimum : "2016-04-01"
  
  "show_all_data": true, (optional), default true
  if false it will show only the date that requested
  
  "window_size": 12, (optional), default 12 (number of months in a year) , since the model using moving average 
  window size is decided to choose interval of rolling mean, 

the result will be returned in JSON file 

---

#### Pythonic Way 
```python 
import requests 


url = 'https://flightpassangerforecast.herokuapp.com/forecast_timeseries'



query = {
  "month_limit": "2021-06-01",
  "show_all_data" : True,
  "window_size": 12
}

def fetchresponses() : 
    response = requests.post(url, json=query)
    print(response)
    
    import pandas as pd 
    data  = pd.read_json(response.json())
    data.to_csv('api_fetch.csv')
    return data
    
fetchresponses()

```
---

#### Postman 
'''
#reference 
# https://towardsdatascience.com/how-to-embed-bootstrap-css-js-in-your-python-dash-app-8d95fc9e599e
layout = dbc.Container(className='api docs', 
                       style = {'background-color':'white'}, 
                       children=[dbc.Row(
                                          [html.H2('API Docs'), 
                                           dcc.Markdown(paragraph)
                                           ]   
                           
                       )
    
    
    
    
])


def render_api_docs() : 
    content = layout
    
    return content
