# Since this was a Regression Problem We will use Linear Regression , Lasso , Rigid , ElasticNet , SVR , DTR, 
# RandomForestRegessor , KNNR ,AdaBoostRegessor , GradientBoostingRegressor , XgboostRegessor  CatBoostRegessor .

import os
import sys
from dataclasses import dataclass
from tabulate import tabulate

from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.logger import logging

# Importing Models for Regression Problem
from sklearn.linear_model import LinearRegression,Lasso,Ridge,ElasticNet
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor

# need to install xgboost and catboost in  requirements.txt first.
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

# Metrics for Measuring the Regression Problem.
from sklearn.metrics import  r2_score,accuracy_score


# In ModelTrainerConfig we will define the path where we have to save the model.pickle file...after model training.
# model.pkl --> contain the best model .

# Now we will use that evalutate metric code from utlies...and also to save the model we need save_object from utiles to save the pickle file.
from src.student_performace_MLProject.utiles.utiles import save_object,evaluate_model

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
            logging.info("Since we have used One Hot Encoding for Categorical data thats why the dim of columns has increased")

            
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
                "XGBoost Regressor": XGBRegressor(),
                "CatBoost Regressor": CatBoostRegressor()
                }
            

            # Lets define the parameters for Hyperparameter Tunning in Models to get the best model with best parameters.

            params = {
                "Linear Regression": {
                    "fit_intercept": [True, False]
                   # "copy_X": [True, False],
                   # "n_jobs": [None, -1, 1, 2]
                    },
                    
                "Rigid Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0]
                    #"fit_intercept": [True, False],
                    # "copy_X": [True, False],
                    # "max_iter": [None, 1000, 5000]
                    },

                "Lasso Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    #"fit_intercept": [True, False],
                    #"precompute": [True, False],
                    #"copy_X": [True, False],
                    #"max_iter": [1000, 5000, 10000]
                },

                "ElasticNet Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0]
                    #"l1_ratio": [0.2, 0.5, 0.7],
                    #"fit_intercept": [True, False],
                    #"precompute": [True, False],
                    #"copy_X": [True, False],
                    #"max_iter": [1000, 5000, 10000]
                },

                "Support Vector Regressor": {
                    "kernel": ['linear', 'poly', 'rbf', 'sigmoid']
                    #"C": [0.1, 1.0, 10.0],
                    #"epsilon": [0.1, 0.2, 0.5],
                    #"gamma": ['scale', 'auto'],
                    #"shrinking": [True, False],
                    #"max_iter": [-1, 1000, 5000]
                },

                "Decision Tree Regressor": {
                    "criterion": ['squared_error', 'absolute_error', 'poisson','friedman_mse'],
                    #"splitter": ['best', 'random'],
                    #"max_depth": [None, 10, 20, 50],
                    #"min_samples_split": [2, 5, 10],
                    #"min_samples_leaf": [1, 2, 4],
                    #"max_features": ['auto', 'sqrt', 'log2', None]
                },

                "RandomForest Regressor": {
                    "n_estimators": [100, 200, 300],
                    #"criterion": ['squared_error', 'absolute_error', 'poisson','friedman_mse'],
                    #"max_depth": [None, 10, 20, 50],
                    #"min_samples_split": [2, 5, 10],
                    #"min_samples_leaf": [1, 2, 4],
                    #"max_features": ['auto', 'sqrt', 'log2',None]
                },

                "AdaBoost Regressor": {
                    #"n_estimators": [50, 100, 200],
                    #"learning_rate": [0.01, 0.1, 1.0],
                    "loss": ['linear', 'square', 'exponential']
                },

                "GradientBoost Regressor": {
                    #"n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0],
                    #"loss": ['ls', 'lad', 'huber', 'quantile'],
                    #"max_depth": [3, 5, 7],
                    #"min_samples_split": [2, 5, 10]
                },

                "XGBoost Regressor": {
                    #"n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.3],
                    #"max_depth": [3, 5, 7],
                    #"subsample": [0.5, 0.8, 1.0],
                    #"colsample_bytree": [0.5, 0.8, 1.0]
                },

                "CatBoost Regressor": {
                    #"iterations": [100, 200, 300],
                    "learning_rate": [0.01, 0.1, 0.3],
                    #"depth": [4, 6, 8],
                    #"l2_leaf_reg": [1, 3, 5],
                    #"border_count": [32, 64, 128]
                }
                }

            # In the 'utils' file, we define a function 'evaluate_model' for assessing the performance of a model.
            # This function takes as inputs: X_train, X_test, y_train, y_test, a list of models, and corresponding parameters params.
            # We utilize GridSearchCV to perform hyperparameter tuning using cross-validation.
            # The function trains each model using GridSearchCV and fits it to the training data.
            # Subsequently, predictions are made on both the training set (for validation) and the test set.
        

            # Now we will use that evalutate metric code from utlies...and also to save the model we need save_object from utiles to save the pickle file.
            # Since the report returned from evaluate_model was report so here we mention is as model_report : dict
        
            model_report : dict = evaluate_model(X_train,y_train,X_test,y_test,models,params)

            # Creating table data
            table_data = []
            for model_name, scores in model_report.items():
                table_data.append([model_name, scores['train_score'], scores['test_score']])

            logging.info("\nModel Performance:")

            # Adding header for the table
            col = ["Model_Name", "Training_Performance", "Testing_Performance"]
            logging.info(tabulate(table_data, headers=col, tablefmt="grid"))
    

            # To get the best model of the dictionary we have this code:
            best_model_score = max(sorted(model_report.values()))
            
            # Based on this best model score we will save the respective name of the model.
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            #Lets also set thresold that if the model performance is less than 60% then Dont save it..

            if best_model_score < 0.6 :
                raise CustomException("No Best Model Found")
            
            logging.info(f"Best Found model on both trainig and testing dataset")

            # Saving the model as pickle file using save_object function from utiles.

            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                object= best_model
            )


            # Now we can make prediction...using X_test data.
            predicted = best_model.predict(X_test)
            r2_sqaure= r2_score(y_test,predicted)

            return r2_sqaure

  

        except Exception as e:
            logging.info("Error has Occured!!!")
            raise CustomException(e,sys)






