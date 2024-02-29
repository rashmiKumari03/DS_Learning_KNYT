import os
import sys
import pickle   # Importing things to save the preprocessing_object into pickle file from data_transformation.py file 
import pymysql
import pandas as pd
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException
import numpy as np


# load_dotenv() Parse a .env file and then load all the variables found as environment variables.
load_dotenv()

# This will load all the env variables from .env
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

def read_sql_data():
    logging.info("Reading SQL database started.....")
    try:
        # Establish the connection to the database and retrieve the data
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )

        logging.info("Connection Established!!!")

      
        df = pd.read_sql_query('SELECT * FROM student_info', mydb)
        print(df.head())

        return df

    except Exception as e:
        logging.error("Custom Exception Executed: {}".format(str(e)))
        raise CustomException(e, sys)
    


# This is to save the object to pickle file..
def save_object(file_path,object):
    try:
        # Defining the path where we have to save this pickle file
        dir_path = os.path.dirname(file_path)

        #making the directory at that respective directory path as mentioned
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj :
            pickle.dump(object,file_obj)
            logging.info(f"Object saved successfully to: {file_path}")

    except Exception as e:
        logging.error(f"Error occurred while saving object to {file_path}: {e}")
        raise CustomException(e,sys)
