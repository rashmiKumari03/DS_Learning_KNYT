import os
import sys
import pymysql
import pandas as pd
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException

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
