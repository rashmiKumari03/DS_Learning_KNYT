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

# To save the object in pickle file --> utiles --> calling function --> save_object()
from src.student_performace_MLProject.utiles.utiles import save_object



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
            data= pd.read_csv(r"C:\Users\Admin\Desktop\DS_Learning_KNYT\02.Student_Performance_ML_E2E_project\artifacts\train.csv")

            print(data.head())
            print(data.shape)
            

            # Defining Numerical and Categorical Feature.
            num_features = data.select_dtypes(exclude='object').columns
            cat_features = data.select_dtypes(include='object').columns


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
        

        
    # Since in the above defination we have created function for transformation of features..now we will call it in this next fucntion.
    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:

            # Reading the train.csv and test.csv from the respective path of train_data_path and test_data_path which we got fromt the last .py file data_ingestion.py file
            # data_ingestion.py --> retuned --> train_data_path , test_data_path
            # So here we are using those path and read the data present there.
             
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            logging.info("Reading the train and test file")


            # Now in same class i want to call the above method here using self.
            preprocessing_object = self.get_data_transformer_object()


            # Diving the dataset to independent and dependent features.
            # We have to do this on both train dataset and test dataset
            # input_features_train_df  is X ,  target_feature_train_df is y .

            
            target_column_name = "math_score"  


            # Diving the train dataset to independent and dependent features.
            input_features_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]


             # Diving the test dataset to independent and dependent features.
            input_features_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying Preprocessing on training and testing dataframe")


            # Most important step : Applying the preprocessor on the training data and testing data.
            # training_data : fit_transform but do testing_data : transform  ( this is to avoid the data leakage)

            input_feature_train_array = preprocessing_object.fit_transform(input_features_train_df)
            input_feature_test_array = preprocessing_object.transform(input_features_test_df)


            # Once i have train_data input & target features : fit and transformed and similarly i have test_data input & target features : transform
            # Now we will combine input and target features for train set and test set using concatenation : using c_ this makes the concate the columns..
            train_array = np.c_[input_feature_train_array , np.array(target_feature_train_df)]
            test_array = np.c_[input_feature_test_array , np.array(target_feature_test_df)]

            logging.info(f"Saved Preprocessing Object means Feature Transformation Done !!!")

            
            # Now at the end of the day this preprocessing happen using preprocessing_object , so we need to save it to pickle file.
            # So to do this common function : saving to pickle we use utiles file...Lets got to utiles file.--> make function  named : save_object()
            # Here in this file lets import that utiles file and call that function...

            # We need these two things to pass to the save_object : to save the object at filepath location
            filepath = self.data_transformation_config.preprocessor_obj_file_path
            object = preprocessing_object

            save_object(filepath,object)



            # We need to return train_array , test_array , file_path_of_preprocessor from config.
            # So that we can use these things in out next .py file in Pipline ie. We can use model_trainer.

            return(train_array,
                   test_array,
                   self.data_transformation_config.preprocessor_obj_file_path)



        except Exception as e:
            logging.info("Custom Exception Raised")
            raise CustomException(e,sys)

