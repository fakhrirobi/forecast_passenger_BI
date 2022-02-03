#inside stats.py 
#import all required packages 

import dash_bootstrap_components as dbc #implementation of bootstrap element in dash 
from dash import Input,Output,dcc # for callback function 
from dash import html # dash wrapper for html component 

import joblib # for loading variable option for dropdown menu 
import numpy as np 
from app import app  #importing Dash instance from app.py 



stats_basic_container_style = {'background-color':'#378dfc','color':'#fcfaff','text-align': 'center'}


#reading all options that will be rendered 
year_list = joblib.load('joblib_file_ref/list_year.joblib')
geo = joblib.load('joblib_file_ref/geo_region.joblib')
operating_airline  = joblib.load('joblib_file_ref/operating_airline.joblib')

#importing all figure maker from src.visualization.py 
from src.visualization import (render_passenger_airlines,
                               render_passenger_overtime,
                               render_passenger_region, 
                               cagr_passanger_overtime,cagr_passanger_per_airlines,cagr_passanger_per_region) 



#https://stackoverflow.com/questions/66069304/run-multiple-dash-apps-with-serve-layout-functions 


#creating dropdown menu for user input
operating_airlines_dropdown = dcc.Dropdown(
                                            id='airline_select', options= [
                                                {'label': airline, 'value': airline} for airline in operating_airline
                                            ], value=operating_airline[0],
                                            placeholder="Select an airline",style={'background-color':'#038cfc','color':'#ffffff'})


region_dropdown = dcc.Dropdown(
                                id='region_select', options= [
                                    {'label': region, 'value': region} for region in geo
                                ], value= geo[0],placeholder="Select a region")
                                
                            
#render statistics page layout
def render_statistics() : 
    select_year = html.Div(dbc.Card([html.H4('Select Range Year : ',className='card-title text-center'),
                                      dcc.RangeSlider(id='year-select',
                                                    min=np.min(year_list),
                                                    max=np.max(year_list),
                                                    value=[np.min(year_list), np.max(year_list)],
                                                    marks={
                                                            2005: {'label': '2005', 'style': {'color': '#77b0b1'}},
                                                            2006: {'label': '2006', 'style': {'color': '#77b0b1'}},
                                                            2007: {'label': '2007', 'style': {'color': '#77b0b1'}},
                                                            2008: {'label': '2008', 'style': {'color': '#77b0b1'}},
                                                            2009: {'label': '2009', 'style': {'color': '#77b0b1'}},
                                                            2010: {'label': '2010', 'style': {'color': '#77b0b1'}},
                                                            2011: {'label': '2011', 'style': {'color': '#77b0b1'}},
                                                            2012: {'label': '2012', 'style': {'color': '#77b0b1'}},
                                                            2013: {'label': '2013', 'style': {'color': '#77b0b1'}},
                                                            2014: {'label': '2014', 'style': {'color': '#77b0b1'}},
                                                            2015: {'label': '2015', 'style': {'color': '#77b0b1'}},
                                                            2016: {'label': '2016', 'style': {'color': '#77b0b1'}}

                                                        },tooltip={"placement": "bottom", "always_visible": True})
                                                    
                    
                                      
                                      ]))
    
    page = dbc.Container(
        
        children= [ 
                dbc.Row(
                    select_year 
                    
                ),
                html.Br(),

                dbc.Row(dbc.Card(html.H5('Statisctics of Total Passenger based on several category',className='card-title text-center'))), 
                html.Br(),
                dbc.Row(
                    [dbc.Col(dbc.Card(
                                        [
                                            html.H6(id='metrics_overall_passanger_growth_header',className='card-title text-center'), 
                                            html.H4(id='metrics_overall_passanger_growth',className='card-title text-center')
                                        ]
                        ,style=stats_basic_container_style),width=4), 
                     dbc.Col(dbc.Card(
                                        [   operating_airlines_dropdown, 
                                            html.H6(id='metrics_airlines_passanger_growth_header',className='card-title text-center'), 
                                            html.H4(id='metrics_airlines_passanger_growth',className='card-title text-center')
                                        ]
                         ,style=stats_basic_container_style),width=4), 
                     dbc.Col(dbc.Card(
                                        [   region_dropdown, 
                                            html.H6(id='metrics_region_passanger_growth_header',className='card-title text-center'), 
                                            html.H4(id='metrics_region_passanger_growth',className='card-title text-center')
                                        ]
                         ,style=stats_basic_container_style),width=4) ] 
                ),
                html.Br(),
                dbc.Row(dbc.Col(
                        dbc.Card(

                                dbc.CardBody(
                                    [
                                        html.H6("Card title", id='passenger_overtime_card_title' , className="card-title text-center"), 
                                        dcc.Graph(id='passenger_overtime')
                                        

                                    ]
                                )
                        ) 
                        # children= [dbc.Col(dcc.Graph(id='passenger_overtime'),width=6), 
                        #             dbc.Col(dbc.Card(dcc.Graph()),width=5), dbc.Col(dbc.Card(dcc.Graph()),width=5)]

                
                ,width=12)),
                html.Br(),
                dbc.Row(
                    [dbc.Col(
                        dbc.Card(

                            dbc.CardBody([html.H6("Title",id='passenger_airlines_card_title' ,className="card-title text-center"), 
                                         dcc.Graph(id='passenger_airlines')]))
                    
                    ,width=6),dbc.Col(
                                                dbc.Card(

                            dbc.CardBody([html.H6("Title",id ='passenger_region_card_title' ,className="card-title text-center"), 
                                         dcc.Graph(id='passenger_region')])
                        )
                    ,width=6)])
        ]
                # ),
                # html.Br(),
                # dbc.Row(
                #     dcc.Graph(id='passenger_region')
                # )]
    )
    
    return page
#callback to adjust timerange in rendering passenger overtime
@app.callback(
    [Output(component_id='passenger_overtime',component_property='figure'),
     Output(component_id='passenger_overtime_card_title',component_property='children')],
    Input(component_id='year-select', component_property='value'),suppress_callback_exceptions=True
)
def update_passanger_overtime(year_range) : 
    text = f'Total Passanger from {year_range[0]} to {year_range[1]}'
    return render_passenger_overtime(range=year_range),text



#callback to adjust timerange in rendering total passenger based on region 
@app.callback(
    [Output(component_id='passenger_region',component_property='figure'),
     Output(component_id='passenger_region_card_title',component_property='children')],
    Input(component_id='year-select', component_property='value'),suppress_callback_exceptions=True
)
def update_passenger_region(year_range) : 
    text = f'Total Passanger per Region  from {year_range[0]} to {year_range[1]}'
    
    return render_passenger_region(range=year_range),text

#callback to adjust timerange in rendering total passenger based on selected airlines 
@app.callback(
    [Output(component_id='passenger_airlines',component_property='figure'),
     Output(component_id='passenger_airlines_card_title',component_property='children')],
    Input(component_id='year-select', component_property='value'),suppress_callback_exceptions=True
)
def update_passenger_airlines(year_range) : 
    text = f'Total Passanger per Airlines Company from {year_range[0]} to {year_range[1]}'
    

    return render_passenger_airlines(range=year_range),text



#callback to count cagr of overtime passenger based on chosen timerange
@app.callback(
    [Output(component_id='metrics_overall_passanger_growth_header',component_property='children'),
     Output(component_id='metrics_overall_passanger_growth',component_property='children')],
    Input(component_id='year-select', component_property='value'),suppress_callback_exceptions=True
)
def update_cagr_passanger_overtime(year_range) : 
    header_text = f'CAGR growth of passanger from {year_range[0]} to {year_range[1]} '
    result = f'{cagr_passanger_overtime(range=year_range)}%'
    
    return header_text,result


#callback to count cagr on total passenger per airlines based on chosen timerange
@app.callback(
    [Output(component_id='metrics_airlines_passanger_growth_header',component_property='children'),
     Output(component_id='metrics_airlines_passanger_growth',component_property='children')],
    [Input(component_id='year-select', component_property='value'),Input(component_id='airline_select', component_property='value')]
    ,suppress_callback_exceptions=True
)
def update_cagr_passanger_airlines(year_range,airline) : 
    header_text = f'CAGR growth of airline : {airline} from {year_range[0]} to {year_range[1]} '
    result = f'{cagr_passanger_per_airlines(year_range,airline)}%'
    
    return header_text,result

#callback to count cagr on total passenger per region  based on chosen timerange
@app.callback(
    [Output(component_id='metrics_region_passanger_growth_header',component_property='children'),
     Output(component_id='metrics_region_passanger_growth',component_property='children')],
    [Input(component_id='year-select', component_property='value'),Input(component_id='region_select', component_property='value')]
    ,suppress_callback_exceptions=True
)
def update_cagr_passanger_region(year_range,region) : 
    header_text = f'CAGR growth of region : {region} from {year_range[0]} to {year_range[1]} '
    result = f'{cagr_passanger_per_region(year_range,region)}%'
    
    return header_text,result