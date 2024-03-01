# Since this was a Regression Problem We will use Linear Regression , Lasso , Rigid , ElasticNet , SVR , DTR, 
# RandomForestRegessor , KNNR ,AdaBoostRegessor , GradientBoostingRegressor , XgboostRegessor  CatBoostRegessor .

import os
import sys
import numpy as np
from urllib.parse import urlparse 

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
from sklearn.metrics import  r2_score,accuracy_score,mean_absolute_error,mean_squared_error

# In ModelTrainerConfig we will define the path where we have to save the model.pickle file...after model training.
# model.pkl --> contain the best model .

# Now we will use that evalutate metric code from utlies...and also to save the model we need save_object from utiles to save the pickle file.
from src.student_performace_MLProject.utiles.utiles import save_object,evaluate_model

# MLflow
import mlflow




@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()




    # Creating evaluation metric :
    
    def eval_metrics(self,actual,pred):
        rmse = np.sqrt(mean_squared_error(actual,pred))
        mae = mean_absolute_error(actual,pred)
        r2 = r2_score(actual,pred)

        return rmse , mae , r2
    


    
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
                    "fit_intercept": [True, False],
                    "copy_X": [True, False],
                    "n_jobs": [None, -1, 1, 2]
                    },
                    
                "Rigid Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    "fit_intercept": [True, False],
                     "copy_X": [True, False],
                     "max_iter": [None, 1000, 5000]
                    },

                "Lasso Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    "fit_intercept": [True, False],
                    "precompute": [True, False],
                    "copy_X": [True, False],
                    "max_iter": [1000, 5000, 10000]
                },

                "ElasticNet Regression": {
                    "alpha": [0.1, 0.5, 1.0, 5.0],
                    "l1_ratio": [0.2, 0.5, 0.7],
                    "fit_intercept": [True, False],
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

            # In the 'utils' file, we define a function 'evaluate_model' for assessing the performance of a model.
            # This function takes as inputs: X_train, X_test, y_train, y_test, a list of models, and corresponding parameters params.
            # We utilize GridSearchCV to perform hyperparameter tuning using cross-validation.
            # The function trains each model using GridSearchCV and fits it to the training data.
            # Subsequently, predictions are made on both the training set (for validation) and the test set.
        

            # Now we will use that evalutate metric code from utlies...and also to save the model we need save_object from utiles to save the pickle file.
            # Since the report returned from evaluate_model was report so here we mention is as model_report : dict
        
            model_report : dict = evaluate_model(X_train,y_train,X_test,y_test,models,params)
            logging.info(f"Model Report Looks Like : {model_report}")

            # Creating table data
            table_data = []
            for model_name, scores in model_report.items():
                table_data.append([model_name, scores['train_score'], scores['test_score']])

            logging.info("\nModel Performance:")

            # Adding header for the table
            col = ["Model_Name", "Training_Performance", "Testing_Performance"]
            logging.info(tabulate(table_data, headers=col, tablefmt="grid"))



            # Getting the Best Model with Best Performance:

            # Initialize a list to store model names and scores
            model_scores = []

            # Iterate over each model
            for model_name, scores in model_report.items():
                train_score = scores['train_score']
                test_score = scores['test_score']
                model_scores.append((model_name, train_score, test_score))

            logging.info(f"Model_score :{model_scores}")

            # Sort models based on test score
            # sorted(model_scores, key=lambda x: x[2], reverse=True) : This means we are sorting the model_scores list which have tuples in it...
            # But Based on what ??? So Based on the test_score denoted by x[2] and reverse = True means in Descending order of Test_score..max to min..
           
            sorted_models = sorted(model_scores, key=lambda x: x[2], reverse=True)
            logging.info(f"Sorted model based on performance {sorted_models}")

            # Print sorted models
            for i, (model_name, train_score, test_score) in enumerate(sorted_models, 1):
                logging.info(f"Model {i}: {model_name}, Train Score: {train_score}, Test Score: {test_score}")

            # Best model
            best_model_name, best_train_score, best_test_score = sorted_models[0]    # Sicne the sorting was max to min based on test score. in descending..so 1st will be obviously the best model
            logging.info(f"\nBest Model: {best_model_name}, Train Score: {best_train_score}, Test Score: {best_test_score}")




            logging.info("Start the MLflow Experiment Tracking part......")
            # MLflow and Dags Code..

            # To get the names of the models from params variable.
            model_names = list(params.keys())
            
            actual_model = ""  # We will update it so initialize it
                
            # Saving the best/actual model , saving parameters of actual model
            for model in model_names:
                if best_model_name == model :
                    actual_model = actual_model + model

            # saving parameter of of best performing model
            param_actual = params[actual_model]



            # Here we have to mention the urls we got from DagsHub..
            mlflow.set_registry_uri("https://dagshub.com/mlprojectrash/DS_Learning_KNYT.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme



            # Lets use the created function (above) for evaluation metric....eval_metrics
            # MLflow Pipeline starts from here For Expermiment Tracking.
            # Install mlflow in requirements.txt and then import it in this file.
            with mlflow.start_run():

                predicted_quantities = actual_model.predict(X_test)

                (rmse , mae , r2) = self.eval_metrics(y_test,predicted_quantities)

                logging.info("logging the best parameters of the model")

                mlflow.log_params(param_actual)
                mlflow.log_metric("rmse",rmse)
                mlflow.log_metrics("mae",mae)
                mlflow.log_metrics("r2",r2)

            # Model registry does not work with file store
            # tracking_url_type_store  : This url is that url which was there in Dags hub..
                
            if tracking_url_type_store != "file":


                # Register the mode
                # There are other ways to use the Model Resgistry
                # This tracking_url_type_store we have mentioned above where links we got from DagsHub are there.

                mlflow.sklearn.log_model(best_model_name,"model", resgistered_model_name=actual_model)
            else:
                mlflow.sklearn.log_model(best_model_name,"model")





            # Let's also set a threshold: if the model performance is less than 60%, then don't save it.
            if best_test_score < 0.6:
                logging.info("Best model's performance is below the threshold. Not saving the model.")
            else:
                logging.info("Best model found on both training and testing datasets.")
                
                # Saving the best model as a pickle file using save_object function from utiles.
                save_object(
                    file_path=self.model_trainer_config.trained_model_file_path,
                    object=models[best_model_name]
                )

                # Now we can make predictions using X_test data.
                logging.info("Predciting the X_test and get the accuracy:")
                predicted = models[best_model_name].predict(X_test)    # For now its X_test but it must be some new data which was not seen by the model...
                r2_square = r2_score(y_test, predicted)

            return r2_square , models[best_model_name]

  

        except Exception as e:
            logging.info("Error has Occured!!!")
            raise CustomException(e,sys)






