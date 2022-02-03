#insied visualization.py
#import all required packages
from datetime import date 
import plotly.express as px #plotting purpose
import plotly.graph_objects as go #plotting purpose
import pandas as pd #data manipulation 
import numpy as np #daa manipulation 
from statsmodels.tsa.stattools import pacf, acf #for autocorrelation purpose


#naming convention 
''' 
render_figurename 
e.g. : 
render_annual_timedata

#standardize color : #7febf5

'''
#function to load and modified data -> converting several values 
def load_data() : 
    data = pd.read_csv('src/data/Air_Traffic_Passenger_Statistics.csv')
    data = data.replace('United Airlines - Pre 07/01/2013', 'United Airlines')
    data['Period'] = data['Activity Period'].astype('str')
    data['Period'] = pd.to_datetime(data['Period'], format='%Y%m')
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


#calcualte cagr
def cagr_passanger_overtime(range,data=data) : 
    data['year'] = data.Period.dt.year
    # passanger_count_group_overtime = data.groupby([ 'Period']).agg(**{'Passenger Total': ('Passenger Count', 'sum')}).reset_index()
    # passanger_count_group_overtime['year'] = passanger_count_group_overtime.Period.year
    year_group = data.groupby([ 'year']).agg(**{'Passenger Annual': ('Passenger Count', 'sum')}).reset_index()    #aggregate first per year
    begin_year = int(range[0]) #year range
    end_year = int(range[1])
    begin_val = year_group.loc[year_group.year==begin_year,'Passenger Annual'].sum() #sum the beginning year value
    end_val = year_group.loc[year_group.year==end_year,'Passenger Annual'].sum() #sum the final  year value
    distance_year = end_year - begin_year
    cagr = np.round((((end_val / begin_val)**(1/float(distance_year))) -1) *100,2)
    return cagr

def render_passenger_overtime(range,data=data) : 
    passanger_count_group_overtime = data.groupby([ 'Period']).agg(**{'Passenger Total': ('Passenger Count', 'sum')}).reset_index()
    
    #filter date based on rangeselector value
    filter_date = (passanger_count_group_overtime.set_index('Period').index.year >= range[0] ) & (passanger_count_group_overtime.set_index('Period').index.year <= range[1]) 
    passanger_count_group_overtime = passanger_count_group_overtime.loc[filter_date]

    ##render the filtered data
    fig1 = px.line(passanger_count_group_overtime.sort_values(by=['Period'], ascending=[True]), x='Period', y='Passenger Total', title='Total Passenger Monthly', template='seaborn')
    fig2 = px.scatter(passanger_count_group_overtime, x='Period', y='Passenger Total', title='Total Passenger Monthly', template='plotly_white')
    fig1.update_traces(line=dict(color = '#050505'))
    fig2.update_traces(line=dict(color = '#050505'))
    #combining two figures
    compiled_figure = go.Figure(data=fig1.data + fig2.data)

    compiled_figure.update_layout(
                                    # title = f'Total Passenger per Month from {range[0]} to {range[1]} ' , title_font_family='montserrat'
        # width=1000,height=500,
        margin=dict(
            l=20,
            r=5,
            b=30,
            t=5,
            pad=4
        ),    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
    
        # paper_bgcolor="#fafffe"
    )
    compiled_figure.update_xaxes(title_text='Month-Year')
    compiled_figure.update_yaxes(title_text='Number of Passenger')
    return compiled_figure





def render_passenger_region(range,data=data) : 
    passanger_count_group_region = data.groupby(['GEO Region', 'Period']).agg(**{'Passenger Total': ('Passenger Count', 'sum')}).reset_index()
    # passanger_count_group_region.set_index('Period',inplace=True)
    filter_date = (passanger_count_group_region.set_index('Period').index.year >= range[0] ) & (passanger_count_group_region.set_index('Period').index.year <= range[1]) 
    passanger_count_group_region = passanger_count_group_region.loc[filter_date]
    pie_chart = px.pie(passanger_count_group_region, values='Passenger Total', names='GEO Region', color='GEO Region', template='ggplot2', color_discrete_map={}, opacity=1,hole=.5)

    pie_chart.update_layout(legend_title_text='Region',
                                    # title = f'Total Passenger per Region {range[0]} to {range[1]}' , title_font_family='montserrat',title_xanchor='left',
                margin=dict(
            l=20,
            r=5,
            b=30,
            t=5,
            pad=4
        ),    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
        , legend=dict(orientation="h",

                    y=0.01,
                    x=0.01
                )
    )
    return pie_chart


def render_passenger_airlines(range,data=data) : 
    passanger_count_group_airlines = data.groupby(['Operating Airline', 'Period']).agg(**{'Passenger_Total': ('Passenger Count', 'sum')}).reset_index()
    # passanger_count_group_airlines.set_index('Period',inplace=True)
    filter_date = (passanger_count_group_airlines.set_index('Period').index.year >= range[0] ) & (passanger_count_group_airlines.set_index('Period').index.year <= range[1]) 
    passanger_count_group_airlines = passanger_count_group_airlines.loc[filter_date]
    
    passanger_count_group_airlines = passanger_count_group_airlines.groupby('Operating Airline').agg(**{'Passenger_Total': ('Passenger_Total', 'sum')}).reset_index()
    passanger_count_group_airlines = passanger_count_group_airlines.sort_values('Passenger_Total')
    fig_airlines = px.treemap(passanger_count_group_airlines, path=['Operating Airline', 'Passenger_Total'], 
                            color='Passenger_Total', 
                            color_continuous_scale='mint', values='Passenger_Total')
    total_passanger = passanger_count_group_airlines['Passenger_Total'].sum()
    passanger_count_group_airlines['pct'] = (passanger_count_group_airlines['Passenger_Total'] / total_passanger) * 100 
    pct = passanger_count_group_airlines['pct'].to_list()
    number_passanger = passanger_count_group_airlines['Passenger_Total'].to_list()
    # to render the text value of tree map we need to create column stack 
    fig_airlines.data[0].customdata = np.column_stack([number_passanger, pct])
    fig_airlines.data[0].texttemplate = "<br>Passanger: %{value:,} <br>Share : %{customdata[1]:.2f}% "

    fig_airlines.update_layout(
                                    # title = f'Total Passenger per Airlines {range[0]} to {range[1]}' , title_font_family='montserrat',title_xanchor='left',
        # width=1000,height=500,
        # margin=dict(
        #     l=20,
        #     r=20,
        #     b=30,
        #     t=50,
        #     pad=4
        # ),
                margin=dict(
            l=20,
            r=5,
            b=30,
            t=5,
            pad=4
        ),    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(orientation="h")
    )


    return fig_airlines
#========================================PREDICTIVE ANALYTICS PAGE 

passanger_data = pd.read_csv('src/data/passanger_total.csv',index_col='Period',parse_dates=['Period'])

def render_resampled_passanger(data = passanger_data) : 
    #return resampled data by month 
    data = data[['Passenger Total']].resample('AS').sum()
    fig = px.line(data.sort_values(by=['Period'], ascending=[True]).reset_index(), x='Period', y='Passenger Total', template='seaborn', title='San Fransisco Airport Total Passenger ( Annually Resampled)')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Total Passanger')
    fig.update_traces(line=dict(color='#1f77b4'))
    fig.update_layout(
                                    title = 'San Fransisco Airport Total Passenger ( Annually Resampled)' , title_font_family='montserrat',title_xanchor='left',
        # width=1000,height=500,
        # margin=dict(
        #     l=20,
        #     r=20,
        #     b=30,
        #     t=50,
        #     pad=4
        # ),
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig 
decompose_ts_data = pd.read_csv('src/data/passanger_total.csv',index_col='Period',parse_dates=['Period'])

def create_acf_pacf_plot(data=decompose_ts_data, plot_pacf=False):
    corr_array = pacf(data.dropna(), alpha=0.05) if plot_pacf else acf(data.dropna(), alpha=0.05)
    lower_y = corr_array[1][:,0] - corr_array[0]
    upper_y = corr_array[1][:,1] - corr_array[0]

    fig = go.Figure()
    [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='#3f3f3f') 
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                   marker_size=12)
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
            fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_xaxes(range=[-1,42])
    fig.update_yaxes(zerolinecolor='#000000')

    fig.update_xaxes(title_text='Lags')
    fig.update_yaxes(title_text='Autocorrelation')
    title='Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
    fig.update_layout(title=title,height=300,margin=dict(
            l=0,
            r=5,
            b=5,
            t=25,
            pad=4
        ),
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return fig

def render_histogram_ts_data() : 
    pd.options.plotting.backend = "plotly"
    data = pd.read_csv('src/data/passanger_total.csv',index_col='Period',parse_dates=['Period'])
    data['Month'] = data.index.strftime('%b')
    data['Year'] = data.index.year

    ts_pivot = data.pivot(index='Year', columns='Month', values='Passenger Total')

    data = data.drop(['Month', 'Year'], axis=1)

    # put the months in order
    month_names = pd.date_range(start='2005-01-01', periods=12, freq='MS').strftime('%b')
    ts_pivot = ts_pivot.reindex(columns=month_names)

    # plot it


    fig = ts_pivot.plot(kind='box')
    fig.update_layout(title='Comparison of Passanger between months',template='ggplot2',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Total Passanger')
    
    return fig


def cagr_passanger_per_airlines(range,airline,data=data) : 
    data['year'] = data.Period.dt.year
    # passanger_count_group_overtime = data.groupby([ 'Period']).agg(**{'Passenger Total': ('Passenger Count', 'sum')}).reset_index()
    # passanger_count_group_overtime['year'] = passanger_count_group_overtime.Period.year
    airlines_group = data.groupby([ 'year','Operating Airline']).agg(**{'Passenger Annual': ('Passenger Count', 'sum')}).reset_index()    
    begin_year = int(range[0])
    end_year = int(range[1])
    begin_val = airlines_group.loc[((airlines_group['Operating Airline']==airline) & (airlines_group['year'] == begin_year)) ,'Passenger Annual'].sum()
    end_val = airlines_group.loc[((airlines_group['Operating Airline']==airline) & (airlines_group['year'] == end_year)) ,'Passenger Annual'].sum()
    distance_year = end_year - begin_year
    cagr = np.round((((end_val / begin_val)**(1/float(distance_year))) -1) *100,2)
    return cagr 


def cagr_passanger_per_region(range,region,data=data) : 
    data['year'] = data.Period.dt.year
    # passanger_count_group_overtime = data.groupby([ 'Period']).agg(**{'Passenger Total': ('Passenger Count', 'sum')}).reset_index()
    # passanger_count_group_overtime['year'] = passanger_count_group_overtime.Period.year
    region_group = data.groupby([ 'year','GEO Region']).agg(**{'Passenger Annual': ('Passenger Count', 'sum')}).reset_index()    
    begin_year = int(range[0])
    end_year = int(range[1])
    begin_val = region_group.loc[((region_group['GEO Region']==region) & (region_group['year'] == begin_year)) ,'Passenger Annual'].sum()
    end_val = region_group.loc[((region_group['GEO Region']==region) & (region_group['year'] == end_year)) ,'Passenger Annual'].sum()
    distance_year = end_year - begin_year
    cagr = np.round((((end_val / begin_val)**(1/float(distance_year))) -1) *100,2)
    return cagr 
    
    

#Predictive Analytics Page 

def render_forecast_figure(forecast_result,window_size) : 
    origin_data= pd.read_csv('src/data/passanger_total.csv',parse_dates=['Period'])
    ''' 
    Parameters : 
    forecast_result = list_of values contain forecast result ( callback result)
    origin_data : pd.Dataframe withour transformation 
        
    '''
    window_size = int(window_size)
    def transform_moving_avg_diff(forecast_result,window_size,num_month=12,origin_data=origin_data) : 
        clone_original_data = origin_data.copy()
        import math 
        #len checking of forecast_result if result only contain 1 : 
        temp_data = pd.DataFrame(data={'Period':[],'Passenger Total' : []})
       
        forecast_result = forecast_result.to_list()
        list_df = [temp_data]
        for idx in range(len(forecast_result)) : 
            z = clone_original_data['Passenger Total'].tail(window_size).rolling(window_size).mean()
            prev_rolling_mean_window = z[z.isnull() ==  False].to_list()[0]
            transformed_value = math.ceil(prev_rolling_mean_window + forecast_result[idx])
            del prev_rolling_mean_window
            
            #generating date by using logic 
            # get last_index = origin_data.index[-1]
            last_month = 3 
            last_year = 2016
            month_step = idx + 1 
            total_month  = month_step + last_month
            print(total_month)
            def year_addition(total_month,num_month) : 
                if total_month <=12 : 
                    return 0
                elif total_month > 12 : 
                     if total_month % 12 == 0 : 
                        multi= math.floor(total_month/num_month)
                        return multi -1 
                     elif total_month % 12 != 0 : 
                        multi= math.floor(total_month/num_month)
                        return multi
                    
            # def add_month(total_month,num_month) : 
            #     if total_month % num_month  == 0 : 
            #         return 12 
            if total_month <= num_month : 
                #because if we yield december it will add to 1 so december will be 2017 
                year_add =  year_addition(total_month,num_month)
                last_year += year_add 
                month_add  = month_step % num_month 
                last_month += month_add
            elif total_month >  num_month : 
                year_add = year_addition(total_month,num_month)
                last_year += year_add 
                month_add  = total_month % num_month if total_month % num_month != 0 else 12 
                #find more proper name 
                add_more_month = last_month + month_add
                last_month -= add_more_month
            date_str = []
            date_str = f'{last_year}-0{abs(last_month)}-01' if abs(last_month) < 10 else f'{last_year}-{abs(last_month)}-01'
            
            # append directly to the dataset 
            append_df = pd.DataFrame(data={'Period':[pd.to_datetime(date_str)],'Passenger Total' : [transformed_value]})
            # clone_original_data.append(append_df)
            clone_original_data = pd.concat([clone_original_data,append_df],axis=0)
            
            # temp_data.append(append_df)
            list_df.append(append_df)
        temp_data = pd.concat(list_df,axis=0)
        
        return temp_data
    transformed_forecast_data = transform_moving_avg_diff(forecast_result,window_size)
    #start creating figure 
    
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        y=origin_data['Passenger Total'], x = origin_data.Period,name='Real Values'
    ))
    figure.add_trace(go.Scatter(
        y=transformed_forecast_data['Passenger Total'], x = transformed_forecast_data.Period,name='Forecast'
    ))
    figure.update_layout(title='Forecast Result ')

    
    
    return figure

