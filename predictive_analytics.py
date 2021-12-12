
import dash_bootstrap_components as dbc 
from dash import Input, Output, html,dcc,State
from dash.exceptions import PreventUpdate
import dash_extensions as de
from datetime import date
from dateutil import relativedelta
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
from  statsmodels.tsa.statespace.sarimax import SARIMAXResults
from dash_extensions import Download
from dash_extensions.snippets import send_file
import pandas as pd 
import numpy as np
import os 
import tempfile
from app import app 



import plotly.graph_objects as go 
from src.visualization import (render_resampled_passanger , 
                               create_acf_pacf_plot, 
                               render_histogram_ts_data, 
                               render_forecast_figure)
from src.load_data import transform_dataset


#COLLECTION of Style 
custom_model_params_style = {'background-color':'#378dfc','color':'#fcfaff','border-radius': '15px','text-align': 'center'}






date_picker = dcc.DatePickerSingle(
    id='month_picker',display_format='MMMM-YYYY', date='2016-04-01',placeholder='Select Month to Forecast', 
    clearable=True,min_date_allowed=date(2016, 4, 1),number_of_months_shown=6
,style={'background-color':'#378dfc'})

time_decomposition_page  = dbc.Container(

    children= [ 
            html.Br(),
            dbc.Row(html.A('Time Series Decomposition')), 
            dbc.Row(
                    children = [dbc.Col(dbc.Card(dcc.Graph(id='passanger_resampled',figure=render_resampled_passanger()))), 
                                dbc.Col(dcc.Graph(id='passanger_histogram',figure=render_histogram_ts_data()))]
                    
            
            ),
            html.Br(),
            dbc.Row(
                children = [ dbc.Col(dcc.Graph(figure=create_acf_pacf_plot())), 
                            dbc.Col(dcc.Graph(figure=create_acf_pacf_plot(plot_pacf=True))) ] 
                            
            ),
            html.Br()
            # dbc.Row(
            #     dcc.Graph(id='passenger_region')
            # )
            ]
)

forecast_page= dbc.Container(
    id='ForecastPage', 
    children= [
        html.Br(), 
        dbc.Row(children=[dbc.Col(
                        dcc.Dropdown(id='Forecast_Menu_Selector', 
                                     options=[{'label':'Number of Passanger overtime', 'value':'Number of Passanger overtime'}, 
                                              {'label':'Number of Passanger Based on Region', 'value':'Number of Passanger Based on Region'}, 
                                              {'label':'Number of Passanger per Airline', 'value':'Number of Passanger per Airline'}], 
                                              value='Number of Passanger per overtime', placeholder='Select What to Forecast'
                                              
                                              
                                              )
            ), 
                dbc.Col(
                    dbc.Card(
                        children = [ 
                                    html.H6('Input Window Size (for rolling mean) : '), 
                                    dcc.Input(id='window_size_input',value=6,min=3,max=24)
                                    ]
                    ))
        
        , 
        html.Br(),
        dbc.Container(
            id='content_forecast'
        ),
        date_picker,
        dcc.Store(id='render_forecast_step'), 
        dbc.Row(
            dbc.Col(dcc.Graph(id='render_forecast_result'))
        ),
        html.H5(id='step')
        
        
        
    ]
)
    ])
custom_model_page= dbc.Container(
    id='Custom Model Page', 
    children= [
        html.Br(), 
        dbc.Row(html.H4('ARMA Components',className='card-title text-center')),
        dbc.Row(
            children=[
            dbc.Col(
            dbc.Card(children=[html.H6('Select AR value'), 
                        dcc.Slider(id='slider_AR',value=1,min=0,max=4,tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose AR :'), 
                        html.H6(id='AR_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='AR_value')],

            style=custom_model_params_style),id='AR Menu'
        ), 
        dbc.Col(
            dbc.Card(children=[html.H6('Select Differencing (d) value'), 
                        dcc.Slider(id='slider_d',value=0,min=0,max=4,tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose Differencing (d) :'), 
                        html.H6(id='d_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='d_value')], style=custom_model_params_style
            ),id='d Menu'
        ), 
        
        dbc.Col(
            dbc.Card(children=[html.H6('Select MA value'), 
                        dcc.Slider(id='slider_MA',value=1,min=0,max=4, 
                                   tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose MA :'), 
                        html.H6(id='MA_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='MA_value')], style=custom_model_params_style
            ),id='MA Menu'
        )
            ]
        ),
        html.Br(),
        dbc.Row(html.H4('Seasonal Components',className='card-title text-center')),
                dbc.Row(
            children=[
            dbc.Col(
            dbc.Card(children=[html.H6('Select Seasonal AR value'), 
                        dcc.Slider(id='slider_seasonalAR',value=1,min=0,max=4,tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose Seasonal AR (P) :'), 
                        html.H6(id='seasonalAR_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='seasonalAR_value')], style=custom_model_params_style
            ),id='AR Menu'
        ), 
        dbc.Col(
            dbc.Card(children=[html.H6('Select Seasonal Differencing (D) value'), 
                        dcc.Slider(id='slider_seasonald',value=0,min=0,max=4,tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose Seasonal Differencing (D) :'), 
                        html.H6(id='seasonald_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='seasonald_value')], style=custom_model_params_style
            ),id='seasonald Menu'
        ), 
        
        dbc.Col(
            dbc.Card(children=[html.H6('Select Seasonal MA value'), 
                        dcc.Slider(id='slider_seasonalMA',value=1,min=0,max=4, 
                                   tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose Seasonal MA :'), 
                        html.H6(id='seasonalMA_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='seasonalMA_value')], style=custom_model_params_style
            ),id='seasonalMA Menu'
        ), 
        dbc.Col(
            dbc.Card(children=[html.H6('Select Periodicity value'), 
                        dcc.Slider(id='slider_seasonalPeriodicity',value=12,min=2,max=24, 
                                   tooltip={"placement": "bottom", "always_visible": True}), 
                        html.H6('You Choose Seasonal MA :'), 
                        html.H6(id='seasonalPeriodicity_slider_pick',className='card-title text-center'), 
                        dcc.Store(id='seasonalPeriodicity_value')], style=custom_model_params_style
            ),id='seasonalMA Menu'
        )
            ]
        ),
        html.Br(),
        dbc.Button("Start Train Custom Model",id='start_train_model_btn', color="primary", className="me-1",style={
            'background-color':'#0ac76c','left':'450px','color':'#f5f7fa'}),
        #METRICS RESULT --------------------------------------------> 
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Card(html.H5('Model Metrics',className='card-title text-center'))),
        html.Br(),
        dbc.Row(
            children = [dbc.Col(
                            dbc.Card(children=[html.H6('MAE Score : ',className='card-title text-center'), 
                                            html.H6(id='MAE Score',className='card-title text-center')
                                                ]
                            )
                            ), 
                       dbc.Col(
                            dbc.Card(children=[html.H6('RMSE Score : ',className='card-title text-center'), 
                                            html.H6(id='RMSE Score',className='card-title text-center')
                                                ]
                            )
                        ), 
                       dbc.Col(
                            dbc.Card(children=[html.H6('MAPE Score : ',className='card-title text-center'), 
                                            html.H6(id='MAPE Score',className='card-title text-center')
                                                ]
                            ))]),
        html.Br(),
        dbc.Row(
            dbc.Col(dbc.Card(
                id='modelplot_lottie'
            ),style={'background-color':'#ffffff'})
        ),
        Download(id="download_custom_model"),
 
        html.Br(),
        dcc.Store(id='store_custom_model'),
        dbc.Container(
            id='content_forecast'
        )
        
        
        
        
    ]
)


def render_predictive_analytics_page() : 
    # lag_slider = dcc.Slider(id='lag_slider', 
    #                     value=12, 
    #                     min=1, 
    #                     max=129)
    
    tabs = html.Div(
        [
            dbc.Tabs(className="nav nav-pills nav-fill",children=
                [
                    dbc.Tab(label="Time Series Decomposition", tab_id="tab-1"),
                    dbc.Tab(label="Forecast", tab_id="tab-2"),
                    dbc.Tab(label="Custom Model Training", tab_id="tab-3"),
                ],
                id="tabs",
                active_tab="tab-1",
            ),
            html.Div(id="content"),
        ]
    )
    
    return tabs


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def tab_navy(pressed_tab):
    if pressed_tab == "tab-1":
        #tab 1 content 
        
        
        return time_decomposition_page
    elif pressed_tab == "tab-2":
        return forecast_page
    elif pressed_tab == "tab-3" : 
        return custom_model_page
    return html.P("This shouldn't ever be displayed...")





@app.callback(
    Output(component_id='content_forecast', component_property='children'), 
    Input(component_id='Forecast_Menu_Selector',component_property='value')
)
def render_forecast_content(what_to_forecast) : 
    if what_to_forecast == 'Number of Passanger overtime' : 
        return html.H3('Test 1')  
    elif what_to_forecast == 'Number of Passanger Based on Region' : 
        return html.H3('Test 2') 
    elif what_to_forecast == 'Number of Passanger per Airline' : 
        return html.H3('Test 3')  
    
@app.callback(
    Output(component_id='render_forecast_step',component_property='data'),
    
    Input(component_id='month_picker',component_property='date')
)
def get_forecast_step(date_value) : 
    date_object = date.fromisoformat(date_value)
    month = date_object.month
    year = date_object.year
    to_forecast_date = []
    # to_forecast_date = date.fromisoformat(f'{year}-0{month}-01') if int(month) <10 else date.fromisoformat(f'{year}-{month}-01')
    if month < 10 : 
        to_forecast_date.append(date.fromisoformat(f'{year}-0{month}-01') )
    elif month >= 10 : 
        to_forecast_date.append(date.fromisoformat(f'{year}-{month}-01') )
    last_date = date.fromisoformat('2016-03-01')
    diff = relativedelta.relativedelta(to_forecast_date[0], last_date)
    forecast_step = diff.months + diff.years * 12
    #create function to load model 
    return forecast_step

@app.callback(
    Output(component_id='render_forecast_result',component_property='figure'),
    Input(component_id='render_forecast_step',component_property='data'), 
    Input(component_id='window_size_input',component_property='value')
    
)
def forecast_timeseries_data(forecast_step,window_size) : 
    #load model 
    loaded_model = SARIMAXResults.load('model/moving_avg_diff_passenger_ovetime_model.pkl')
    
    # forecast using step
    forecast_result  = loaded_model.forecast(steps=forecast_step)
    #store result in a variable 
    
    figure = render_forecast_figure(forecast_result,window_size)
    return figure
@app.callback(
    Output(
        component_id='AR_slider_pick',component_property='children'
    ), 
    Output(component_id='AR_value',component_property='data'), 
    Input(component_id='slider_AR',component_property='value')
)
def AR_Slider_pick(AR_value) : 
    
    return f'{AR_value}',AR_value


@app.callback(
    Output(
        component_id='MA_slider_pick',component_property='children'
    ), 
    Output(component_id='MA_value',component_property='data'), 
    Input(component_id='slider_MA',component_property='value')
)
def MA_Slider_pick(MA_VALUE) : 
    
    return f'{MA_VALUE}',MA_VALUE


@app.callback(
    Output(
        component_id='d_slider_pick',component_property='children'
    ), 
    Output(component_id='d_value',component_property='data'), 
    Input(component_id='slider_d',component_property='value')
)
def d_Slider_pick(d_order) : 
    
    return f'{d_order}',d_order


@app.callback(
    Output(
        component_id='seasonalAR_slider_pick',component_property='children'
    ), 
    Output(component_id='seasonalAR_value',component_property='data'), 
    Input(component_id='slider_seasonalAR',component_property='value')
)
def SeasonalAR_Slider_pick(seasonalAR_value) : 
    
    return f'{seasonalAR_value}',seasonalAR_value


@app.callback(
    Output(
        component_id='seasonalMA_slider_pick',component_property='children'
    ), 
    Output(component_id='seasonalMA_value',component_property='data'), 
    Input(component_id='slider_seasonalMA',component_property='value')
)
def SeasonalMA_Slider_pick(seasonalMA_VALUE) : 
    
    return f'{seasonalMA_VALUE}',seasonalMA_VALUE


@app.callback(
    Output(
        component_id='seasonald_slider_pick',component_property='children'
    ), 
    Output(component_id='seasonald_value',component_property='data'), 
    Input(component_id='slider_seasonald',component_property='value')
)
def Seasonald_Slider_pick(seasonald_order) : 
    
    return f'{seasonald_order}',seasonald_order


@app.callback(
    Output(
        component_id='seasonalPeriodicity_slider_pick',component_property='children'
    ), 
    Output(component_id='seasonalPeriodicity_value',component_property='data'), 
    Input(component_id='slider_seasonalPeriodicity',component_property='value')
)
def Seasonald_Periodicity_pick(periodicity) : 
    
    return f'{periodicity}',periodicity

@app.callback(
    Output(component_id='download content',component_property='data'), 
    Input(component_id='download_cs_model',component_property='n_clicks'),
    Input(component_id='store_custom_model',component_property='data')
)
def download_custom_model(button_click,file) : 
    if button_click : 
        dcc.send_file(file)  

@app.callback(
    [Output(component_id='modelplot_lottie',component_property='children'), 
    Output(component_id='MAE Score',component_property='children'), 
    Output(component_id='RMSE Score',component_property='children'), 
    Output(component_id='MAPE Score',component_property='children')],
    #Output(component_id='store_custom_model',component_property='data')],
    [Input(component_id='AR_value',component_property='data'),
    Input(component_id='MA_value',component_property='data'),
    Input(component_id='d_value',component_property='data'),
    Input(component_id='seasonalAR_value',component_property='data'),
    Input(component_id='seasonalMA_value',component_property='data'),
    Input(component_id='seasonald_value',component_property='data'),
    Input(component_id='seasonalPeriodicity_value',component_property='data'),
    Input(component_id='start_train_model_btn',component_property='n_clicks')],suppress_callback_exceptions=True
)
def train_custom_model(p,d,q,P,D,Q,s,button_click) : 
    if button_click is not None: 
        from sklearn import metrics 
        
        data = pd.read_csv('src/data/passanger_total.csv',index_col='Period',parse_dates=['Period'])
        data = transform_dataset(data=data)
        print(data.columns)
        model = sm.tsa.SARIMAX(data['moving_avg_diff'], order=(p,d,q),
                                seasonal_order=(P,D,Q,s)
                        )
        results = model.fit()
        
        yhat = results.fittedvalues
        
        figure = go.Figure()
        figure.add_trace(
            go.Scatter(x=data.index,y=data['moving_avg_diff'],name='original values')
        )
        figure.add_trace(
            go.Scatter(x=data.index,y=yhat,name='fitted values')
        )
        figure.update_layout(title='Custom Model Results')
        
        MAE_ = metrics.mean_absolute_error(data['moving_avg_diff'],yhat)
        RMSE_  = metrics.mean_squared_error(data['moving_avg_diff'],yhat)
        MAPE_ = metrics.mean_absolute_percentage_error(data['moving_avg_diff'],yhat)
        print(MAPE_)
        print(MAE_)
        print(RMSE_)
        tempdir = tempfile.mkdtemp()
        # filename = os.path.join('custom_model.pkl')
        results.save('custom_model.pkl')
        graph = dbc.Container(children=[dbc.Row(dcc.Graph(id='plot_custom_model',figure=figure)), 
                                        html.Br()
                                        ])
        import pickle 
        with open('custom_model.pkl', 'rb') as pickle_file:
            content = pickle.load(pickle_file)
        print(type(content))
        
        
        
        return graph,f'{MAE_}', f'{RMSE_}',f'{MAPE_}'
    
    else : 
        options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
        lottie_url = 'https://assets3.lottiefiles.com/datafiles/bEYvzB8QfV3EM9a/data.json'
        lottie_gif = dbc.Row(children=[html.Br(),html.Br(),html.H3('You Have Not Enter The Model Params',style={'text-align': 'center','color':'#e60b16'}),
                                       dbc.Row(de.Lottie(options=options, width="25%", height="25%", url=lottie_url))
                                        ],style={'background-color':'#ffffff','border-radius':'15px'})
        return lottie_gif,'-','-','-'
    


# @app.callback(
#     Output(component_id='download_custom_model',component_property=''),
#     Input(component_id='',component_property=''), 
#     State(component_id='',component_property='')
        
#     )

# def download_custom_file() : 
#     send_file("custom_model.png")