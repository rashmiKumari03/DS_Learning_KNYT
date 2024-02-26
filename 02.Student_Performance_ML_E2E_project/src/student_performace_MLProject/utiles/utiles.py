
# We are using utiles file for generic functionality...and here we will write the code to  get the data from database.
# READING SQL DATA: and we will directly take paramters needed from .env


import os
import sys

from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException
import pandas as pd
import pymysql

from dotenv  import load_dotenv
load_dotenv()  # This will load all the env variable from .env


host=os.getenv("host")
user=os.getenv("user")
password = os.getenv("password")
db=os.getenv("db")


def read_sql_data():
    logging.info("Reading SQL database started.....")
    try:
        # Establish the connect to connect the db and get the data.
    
        mydb= pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )

        logging.info("Connection Established!!!",mydb)
        df=pd.read_sql_query('Select * from student_info',mydb)
        print(df.head())

        return df

    except Exception as e:
        logging.info("Custom Exception Executed")
        raise CustomException(e,sys)
