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


from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


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


# In the 'utils' file, we define a function 'evaluate_model' for assessing the performance of a model.
# This function takes as inputs: X_train, X_test, y_train, y_test, a list of models, and corresponding parameters params.
# We utilize GridSearchCV to perform hyperparameter tuning using cross-validation.
# The function trains each model using GridSearchCV and fits it to the training data.
# Subsequently, predictions are made on both the training set (for validation) and the test set.
    
def evaluate_model(X_train,y_train,X_test,y_test,models,param):
    try:
        report = {}

        logging.info(f"Number of Models :{len(list(models))}")
       

        for i in range(len(models)):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            parameters = param[model]

            logging.info(f"Model Name: {model_name}, Model Object: {model}")

            # Do GridSearchCV on model with parameters
            gs = GridSearchCV(model, parameters)
            gs.fit(X_train, y_train)

            # Set the best parameters found by GridSearchCV
            model.set_params(**gs.best_params_)

            # Train the model
            model.fit(X_train, y_train)

            # Make predictions on training and test sets
            y_train_pred = model.predict(X_train)  # For Validation
            y_test_pred = model.predict(X_test)

            # Calculate R^2 score for training and test sets
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            # Store model performance scores in the report dictionary
            report[model_name] = {'train_score': train_model_score, 'test_score': test_model_score}

        return report


    except Exception as e:
        logging.info("Error has Occured!!!")
        raise CustomException(e,sys)
