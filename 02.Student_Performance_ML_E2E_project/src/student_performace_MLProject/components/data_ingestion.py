
# Database->data->train_test_split_format
# Get the Data in MySQL Database and read the data from MySQL .
# Mysql--->Read in local--> Train_test_split-->Dataset

import os    # To get the path and make paths
import sys   # To handle customexception
from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split

# Firstly we need to Get the data from MySQL database & we need to read it in local.
# Then We Have to understand what we want as output : 1.Train dataset 2.Test dataset
# For getting these two as output --> What would be the inputs provided? 
# Inputs : 1. Dataframe(we got from MySQL) 2.Train Data Path 3.Test Data Path

# This is to use read_sql_data from utiles , which will read the data from db.
from src.student_performace_MLProject.utiles.utiles import read_sql_data

from dataclasses import dataclass # This is to initialize the input parameter which we are trying to provide.

@dataclass
class DataIngestionConfig:

    #Firslty we want to save the raw means entire data also (before splitting)
    raw_data_path:str = os.path.join('artifacts','raw.csv')

    # Path of traindata , Path of testdata
    train_data_path:str=os.path.join('artifacts','train.csv')   # We haev already created a folder artifacts and in this 
                                                                # we are supposed to save the train data and test data
    # Similarly for testdata path
    test_data_path:str=os.path.join('artifacts','test.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()   # We are getting the input parameters from DataIngestionConfig.

    def initiate_data_ingestion(self):
        # First step of data ingestion: Reading from mysql database..
        # FIrstly Write try except block..and raise CustomeException from that.


        try:

            # Reading code
            # We need to use utiles file read_sql_data() function to read the data...
            df = read_sql_data()    # This was raw data..

            # Make config in .env folder (create it) and code will be there in utiles file.
            logging.info("Reading Completed from the MySQL Database")

            # We got some dataframe from reading so --> we need save that data into raw.csv in artifacts folder.
            # Suppose if artifacts is not present then make it how..using the path...any of the 3 it will ultimatly make artifacts folder.

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)  # We are getting the dir path..from ingestion (input paths)-->called any path.
            # Since we have raw data from df...we will convert it into csv and save it the the specific path we provided as input.
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            # Now we will do train test split using this data...use sklearn->train_test_split
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            # Since from above we got data into train_set and test_set so we need to save it into the paths.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header= True)
            
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header= True)


            return (self.ingestion_config.train_data_path,
                    self.ingestion_config.test_data_path)
                    
        
            
        except Exception as e:
            logging.info("Custom Exception Executed")
            raise CustomException(e,sys)
