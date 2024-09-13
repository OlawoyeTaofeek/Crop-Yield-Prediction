import pandas as pd
import requests
import logging
import sqlalchemy
from sqlalchemy import create_engine, text


# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_db_engine(db_path):
    """
    Create a SQLAlchemy database engine.

    Parameters:
    
    - db_path (str): Database connection string.

    Returns:
    - sqlalchemy.engine.Engine: Database engine object
        
    Examples:
       >>> create_db_engine('sqlite:///example.db')
    """
    try:
        engine = create_engine(db_path)
        
        with engine.connect() as conn:
            pass 
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well'
    
    except ImportError as e:
        # logger.error(f"Failed to create database engine. Error")
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e
    
    
    
def query_data(engine, sql_query: str) -> pd.DataFrame:
    """     
    Execute a SQL query on the provided database engine and return the result as a DataFrame.
   
    Returns a DataFrame corresponding to the result set of the query string with the help of the specified database engine.
    
    Parameters:
    - engine (sqlalchemy.engine.Engine): Database engine object.
    - sql_query (str): SQL query string.

    Returns:
    - pandas.DataFrame: Result of the SQL query as a DataFrame after using the pandas.read_sql_query.
        
    Examples:
       >>> query_data(engine, text("SELECT * FROM example_table"))
    """
    
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
            
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e


    
def read_from_web_CSV(URL: str) -> pd.DataFrame:
    """
    # summary
    Read a CSV file from a given URL and return its contents as a DataFrame.

    ### Args:
        URL (str): URL pointing to a CSV file.

    ### Raises:
        pd.errors.EmptyDataError: If the URL does not point to a valid CSV file.
        ValueError: If there's an issue retrieving data from the URL or if the response status code is not 200.
        Exception: If there's a general error during the CSV reading process.

    ### Returns:
       pandas.DataFrame: DataFrame containing the CSV data.
       
    ### Examples:
    >>> read_from_web_CSV("https://raw.githubusercontent.com/LambdaSchool/DS-Unit-2-Applied-Modeling/master/data/chipotle.tsv")
    """
    

    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e