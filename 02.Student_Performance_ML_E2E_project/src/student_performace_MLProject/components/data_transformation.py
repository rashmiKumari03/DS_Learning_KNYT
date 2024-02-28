# Data Transformation is more about the feature engineering.
# Output of this will be the pkl file...


import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline

from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.logger import logging


@dataclass    # This basically stores the information of class here path.
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')    # We are defining a path to save pickle file at this location


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()   # So that we can get the path in a variable (where we are thinking to save the pkl) .

    
    # This get_data_transformer_object() function is responsible for doing data transformation/feature engineering
    def get_data_transformer_object(self):

        '''
        This function is responsible for data transformation or feature engineering
        '''

        try:
             
            # Reading the data (training data)
            data = pd.read_csv('.\artifacts\train.csv')
            print(data.head())
            print(data.shape)
            
            # Independent and Dependent Variables.
            X = data.iloc[]
           
            



            # Defining Numerical and Categorical Feature.
            num_features = X.select_dtypes(exclude='object').columns
            cat_features = X.select_dtypes(incude='object').columns


            # Suppose in case we have missing values in our data or may be new data coming
            # having some missing values so to handle it we need some imputation
            # We use SimpleImputer with Pipeline...So that....Just After Imputation-->Column Transformation Takes Place in Pipeline.

            # Pipeline for : numerical feature and for categorical features

            num_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='median')),
                ("scaler",StandardScaler())
            ])


            cat_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='most_frequent')),
                ("Ohe",OneHotEncoder()),           # Here values comes in 0 to 1 but just additonal we normalize we use StandardScaler (we can skip it too)
                ("scaler",StandardScaler(with_mean=False))

            ])

            logging.info(f"Numerical Columns:{ num_features}")
            logging.info(f"Categorical Columns:{ cat_features}")


            # Since We have num_pipeline to handle numerical features and cat_pipeline to handle Categorical features.
            # But at the end of the dat : we need to combine these two..for that we use ColumnTransformer.

            preprocessor = ColumnTransformer([
                ("Numerical_Pipeline_to_handle_numerical_values",num_pipeline,num_features),
                ("Categorical_Pipeline_to_handle_numerical_values",cat_pipeline,cat_features)
            ])


            return preprocessor     # This preprocessor handled num and cat feature with all column transformations.
                                    # Therefore :get_data_transformer_object() --> returns Feature Transformation--> preprocessor


         





            


















        except Exception as e:
            logging.info("Custom Exception Executed")
            raise CustomException(e,sys)


