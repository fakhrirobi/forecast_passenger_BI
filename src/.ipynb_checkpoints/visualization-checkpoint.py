import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd 



#naming convention 
''' 
render_figurename 
e.g. : 
render_annual_timeseries

#standardize color : #7febf5

'''
def load_data() : 
    data = pd.read_csv('Air_Traffic_Passenger_Statistics.csv')
    data = data.replace('United Airlines - Pre 07/01/2013', 'United Airlines')
    data['Period'] = data['Activity Period'].astype('string')
    data = data.drop_duplicates(keep='first')
    data = data.drop(columns=['Activity Period'])
    
    # all geo data 
    data['GEO Region'] = data['GEO Region'].replace('Canada', 'North America')
    data['GEO Region'] = data['GEO Region'].replace('US', 'North America')
    data['GEO Region'] = data['GEO Region'].replace('Australia / Oceania', 'Australia')
    data['GEO Region'] = data['GEO Region'].replace('Middle East', 'Asia')
    data['GEO Region'] = data['GEO Region'].replace('Central America', 'South America')
    data['GEO Region'] = data['GEO Region'].replace('Mexico', 'South America')
    
    
    return data 

data = load_data()

passanger_count_group_period = data.groupby(['Period']).agg(**{'Passenger Count_sum': ('Passenger Count', 'sum')}).reset_index()
passanger_count_group_period['Period'] = pd.to_datetime(passanger_count_group_period['Period'], format='%Y%m')

passanger_count_group_region = data.groupby(['GEO Region']).agg(**{'Passenger Count_sum': ('Passenger Count', 'sum')}).reset_index()



passanger_count_group_airlines = data.groupby(['Operating Airline']).agg(**{'Passenger_Total': ('Passenger Count', 'sum')}).reset_index()

def render_passenger_overtime(data=passanger_count_group_period) : 
    fig1 = px.line(data.sort_values(by=['Period'], ascending=[True]), x='Period', y='Passenger Count_sum', title='Total Passenger Monthly', template='seaborn')
    fig2 = px.scatter(data, x='Period', y='Passenger Count_sum', title='Total Passenger Monthly', template='plotly_white')
    fig1.update_traces(line=dict(color = '#050505'))
    fig2.update_traces(line=dict(color = '#050505'))
    compiled_figure = go.Figure(data=fig1.data + fig2.data)

    compiled_figure.update_layout(
                                    title = 'Total Passenger per Month' , title_font_family='montserrat',title_xanchor='left',
        width=1000,height=500,
        margin=dict(
            l=20,
            r=20,
            b=30,
            t=50,
            pad=4
        ),
        paper_bgcolor="LightSteelBlue"
    )
    compiled_figure.update_xaxes(title_text='Month-Year')
    compiled_figure.update_yaxes(title_text='Number of Passenger')
    return compiled_figure





def render_passenger_region(data=passanger_count_group_region) : 
    fig = px.pie(data, values='Passenger Count_sum', names='GEO Region', color='GEO Region', template='ggplot2', title='Passenger Proportion divided by Continent')
    return fig


def render_passenger_airlines(data=passanger_count_group_airlines) : 
    fig_airlines = px.treemap(data, path=['Operating Airline', 'Passenger_Total'], 
                            branchvalues='total', color='Passenger_Total', 
                            color_continuous_scale='mint', values='Passenger_Total')

    fig_airlines.update_layout(
                                    title = 'Total Passenger per Airlines' , title_font_family='montserrat',title_xanchor='left',
        width=1000,height=500,
        margin=dict(
            l=20,
            r=20,
            b=30,
            t=50,
            pad=4
        ),
        paper_bgcolor="LightSteelBlue"
    )


    return fig_airlines


