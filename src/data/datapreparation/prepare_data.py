


from typing import Type
import pandas as pd 
import os 
import sys
from generate_modified_data import logger

logger = logger

class DataWrangler : 
    #loading the dataset 
    
    def load_data(self) : 
        
        filepath = 'Air_Traffic_Passenger_Statistics.csv'
        data = pd.read_csv(filepath)
        #change_back_to_default_path 
        return data 
    
    def prepare_eda_data(self,dataframe) : 
        '''
        Parameters : 
        Dataframe : pandas dataframe
        
        '''
        data = dataframe.copy()
        #replacing airline value
        data = data.replace('United Airlines - Pre 07/01/2013', 'United Airlines')
        #changing period format from string to datetime
        data['Period'] = data['Activity Period'].astype('string')
        data['Period'] = pd.to_datetime(data['Period'], format='%Y%m')
        #dropping duplicates
        data = data.drop_duplicates(keep='first')
        #dropping Activity Period columns
        data = data.drop(columns=['Activity Period'])
        #replacing value of each GEO Region values
        data['GEO Region'] = data['GEO Region'].replace('Canada', 'North America')
        data['GEO Region'] = data['GEO Region'].replace('US', 'North America')
        data['GEO Region'] = data['GEO Region'].replace('Australia / Oceania', 'Australia')
        data['GEO Region'] = data['GEO Region'].replace('Middle East', 'Asia')
        data['GEO Region'] = data['GEO Region'].replace('Central America', 'South America')
        data['GEO Region'] = data['GEO Region'].replace('Mexico', 'South America')
        return data
    
    def prepare_forecast_data(self,dataframe,logger=logger) : 
        #check if the dataframe is pd.Dataframe
        if isinstance(dataframe, pd.DataFrame):
            data = dataframe.copy()
            data = data.groupby(['Period']).agg(**{'Total Passenger': ('Passenger Count', 'sum')})
            data = data.rename(columns={'Period': 'Activity Period'})
            return data
                
                
        else :  
            raise TypeError('the dataframe argument should be pandas Dataframe')
            logger.error('TypeError : input should be pandas Dataframe')
            
        