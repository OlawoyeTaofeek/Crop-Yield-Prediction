import pandas as pd
from data_ingestion import create_db_engine, query_data, read_from_web_CSV
import logging
from src.utils import config_params

class FieldDataProcessor:

    def __init__(self, config_params, log_level="INFO"):  # Make sure to add this line, passing in config_params to the class 
        self.db_path = config_params['db_path']
        self.sql_query = config_params["sql_query"]
        self.columns_to_rename = config_params["columns_to_rename"]
        self.values_to_rename = config_params["values_to_rename"]
        self.weather_map_data = config_params["weather_mapping_csv"]
        self.weather_station_data = config_params["weather_csv_path"]

        self.initialize_logging(log_level)
        
        # We create empty objects to store the DataFrame and engine in
        self.df = None
        self.engine = None
        
    # This method enables logging in the class. 
    def initialize_logging(self, logging_level):
        """
        ### Summary
        Sets up logging for this instance of FieldDataProcessor.
        
        
        """
        logger_name = __name__ + ".FieldDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False  # Prevents log messages from being propagated to the root logger

        # Set logging level
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":  # Option to disable logging
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO  # Default to INFO

        self.logger.setLevel(log_level)

        # Only add handler if not already added to avoid duplicate messages
        if not self.logger.handlers:
            file_handler = logging.FileHandler('code-info.log', mode='w')  # Set mode to 'w' for append
            # file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            ch = logging.StreamHandler()  # Create console handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        # Use self.logger.info(), self.logger.debug(), etc.


    # DataFrame methods 
    def ingest_sql_data(self):
        # First we want to get the data from the SQL database
        self.engine = create_db_engine(self.db_path)
        self.df = query_data(self.engine, self.sql_query)
        self.logger.info("Sucessfully loaded data.")
        return self.df
    
    def rename_columns(self):
        # Annual_yield and Crop_type must be swapped
        # Temporarily rename one of the columns to avoid a naming conflict
        
        temp_name = "Annual_yield"
        while temp_name in self.df.columns:
            temp_name += "_"
            
        
         # Extract the columns to rename from the configuration
        column1, column2 = list(self.columns_to_rename.keys())[0], list(self.columns_to_rename.values())[0] 

        # Perform the swap
        self.df = self.df.rename(columns={column1: temp_name, column2: column1})
        self.df = self.df.rename(columns={temp_name: column2})  
        
        self.logger.info(f"Swapped columns: {column1} with {column2}")  

    def apply_corrections(self, column_name='Crop_type', abs_column='Elevation'):
        # Check if the abs_column exists before applying absolute value
        if abs_column in self.df.columns:
            self.df[abs_column] = self.df[abs_column].abs()
            # self.logger.info(f"Applied absolute value correction to {abs_column}")
            
        else:
            self.logger.warning(f"{abs_column} column not found. Skipping absolute value correction.")
            
        # Correct the crop strings, e.g., 'cassaval' -> 'cassava'
        self.df[column_name] = self.df[column_name].apply(lambda crop: crop.strip())
        self.df[column_name] = self.df[column_name].apply(lambda crop: self.values_to_rename.get(crop, crop))


    
    def weather_station_mapping(self):
        # Merge the weather station data to the main DataFrame
        weather_df = read_from_web_CSV(self.weather_map_data)
        # self.df = pd.merge(self.df, weather_df, on=merge_column, how='left')
        
        # # Drop unnecessary columns
        # self.df = self.df.drop(columns=["Unnamed: 0"])
        
        # return self.df
        return weather_df


    def process(self):
    # This process calls the correct methods and applies the changes, step by step. This is the method we will call, and it will call the other methods in order.
        self.df = self.ingest_sql_data()
        #Insert your code here
        
        # 3. Rename columns
        self.rename_columns()
        
        # 4. Apply corrections
        self.apply_corrections()

        weather_df = self.weather_station_mapping()
    
        self.df = pd.merge(self.df, weather_df, how='left', on="Field_ID")
        self.df.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
        
        return self.df
