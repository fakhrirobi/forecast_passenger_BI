import prepare_data

# importing module
import logging
 
# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()


def begin_process() : 
    wrangler = prepare_data.DataWrangler()


    data = wrangler.load_data()

    eda_data = wrangler.prepare_eda_data(data)

    eda_data.to_csv('prepare_for_eda.csv')
    print(eda_data.head(4))
    logger.info("Finished preparing data for EDA")


    
    # / TODO : 
    # the output should contain two columns : Activity Period and Passengger Total 
    forecast_data = wrangler.prepare_forecast_data(eda_data)
    print(forecast_data.head(4))
    forecast_data.to_csv('forecast_data.csv',index=False)
    logger.info("Finished preparing data for forecast data")
if __name__ == '__main__' : 
    begin_process()