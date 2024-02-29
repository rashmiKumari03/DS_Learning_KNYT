# Since this was a Regression Problem We will use Linear Regression , Lasso , Rigid , ElasticNet , SVR , DTR, 
# RandomForestRegessor , KNNR ,AdaBoostRegessor , GradientBoostingRegressor , XgboostRegessor  CatBoostRegessor .

import os
import sys
from dataclasses import dataclass

from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.logger import logging

# Importing Models for Regression Problem
from sklearn.linear_model import LinearRegression,Lasso,Ridge,ElasticNet
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor

# need to install xgboost and catboost in  requirements.txt first.
from xgboost import XGBoostRegressor
from catboost import CatBoostRegressor

# Metrics for Measuring the Regression Problem.
from sklearn.metrics import  r2_score,accuracy_score


# In ModelTrainerConfig we will define the path where we have to save the model.pickle file...after model training.
# model.pkl --> contain the best model .

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    
    # As input we need to pass : train_array , test_array (ie. transformed data)
    def initiate_model_trainer(self,train_array,test_array):

        try:
            logging.info("Split the training and test input data")
            
            # Since in transformation we have concatenated target feature at last of X_train and similarly for X_test So -1 : means target feature.

            X_train , y_train = train_array[:,:-1] , train_array[:,-1]   # X_train ie. Training_inputs , y_train ie. Training_target
            X_test , y_test = test_array[:,:-1] , test_array[:,-1]   # X_test ie. Testing_inputs , y_test ie. Testing_target

            logging.info(f"Shape of the Training Input Feature is: {X_train.shape}\nTraining Target Feature is:{y_train.shape}")
            logging.info(f"Shape of the Testing Input Feature is: {X_test.shape}\nTesting Target Feature is:{y_test.shape}")

            
            # Making List of Models in Dictionary Form.

            models = {
                "Linear Regression": LinearRegression(),
                "Rigid Regression": Ridge(),
                "Lasso Regression": Lasso(),
                "ElasticNet Regression": ElasticNet(),
                "Support Vector Regressor": SVR(),
                "Decision Tree Regressor": DecisionTreeRegressor(),
                "RandomForest Regressor": RandomForestRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "GradientBoost Regressor": GradientBoostingRegressor(),
                "XGBoost Regressor": XGBoostRegressor(),
                "CatBoost Regressor": CatBoostRegressor()
                }
            

            # Lets define the parameters for Hyperparameter Tunning in Models to get the best model with best parameters.

            params = {
                "Linear Regression": {
                    "fit_intercept": [True, False],
                    "normalize": [True, False],
                    "copy_X": [True, False],
                    "n_jobs": [None, -1, 1, 2]
                    },
                    
                "Rigid Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    "fit_intercept": [True, False],
                    "normalize": [True, False],
                    "copy_X": [True, False],
                    "max_iter": [None, 1000, 5000]
                    },

                "Lasso Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    "fit_intercept": [True, False],
                    "normalize": [True, False],
                    "precompute": [True, False],
                    "copy_X": [True, False],
                    "max_iter": [1000, 5000, 10000]
                },

                "ElasticNet Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    "l1_ratio": [0.2, 0.5, 0.7],
                    "fit_intercept": [True, False],
                    "normalize": [True, False],
                    "precompute": [True, False],
                    "copy_X": [True, False],
                    "max_iter": [1000, 5000, 10000]
                },

                "Support Vector Regressor": {
                    "kernel": ['linear', 'poly', 'rbf', 'sigmoid'],
                    "C": [0.1, 1.0, 10.0],
                    "epsilon": [0.1, 0.2, 0.5],
                    "gamma": ['scale', 'auto'],
                    "shrinking": [True, False],
                    "max_iter": [-1, 1000, 5000]
                },

                "Decision Tree Regressor": {
                    "criterion": ['squared_error', 'absolute_error', 'poisson','friedman_mse'],
                    "splitter": ['best', 'random'],
                    "max_depth": [None, 10, 20, 50],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": ['auto', 'sqrt', 'log2', None]
                },

                "RandomForest Regressor": {
                    "n_estimators": [100, 200, 300],
                    "criterion": ['squared_error', 'absolute_error', 'poisson','friedman_mse'],
                    "max_depth": [None, 10, 20, 50],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": ['auto', 'sqrt', 'log2',None]
                },

                "AdaBoost Regressor": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0],
                    "loss": ['linear', 'square', 'exponential']
                },

                "GradientBoost Regressor": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0],
                    "loss": ['ls', 'lad', 'huber', 'quantile'],
                    "max_depth": [3, 5, 7],
                    "min_samples_split": [2, 5, 10]
                },

                "XGBoost Regressor": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.3],
                    "max_depth": [3, 5, 7],
                    "subsample": [0.5, 0.8, 1.0],
                    "colsample_bytree": [0.5, 0.8, 1.0]
                },

                "CatBoost Regressor": {
                    "iterations": [100, 200, 300],
                    "learning_rate": [0.01, 0.1, 0.3],
                    "depth": [4, 6, 8],
                    "l2_leaf_reg": [1, 3, 5],
                    "border_count": [32, 64, 128]
                }
}



        

        






            
            

            



            

            



        except Exception as e:
            logging.info("Error has Occured!!!")
            raise CustomException(e,sys)






