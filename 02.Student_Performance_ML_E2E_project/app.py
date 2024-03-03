# We know the location of logger.py so lets call it from there.
import sys

from src.student_performace_MLProject.logger import logging

from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.components.data_ingestion import DataIngestion
from src.student_performace_MLProject.components.data_transformation import DataTransformation

from src.student_performace_MLProject.components.model_trainer import ModelTrainer

import warnings
warnings.filterwarnings('ignore')


# To check whether things are working file...lets make it.
if __name__ == "__main__":
    logging.info("The Exectuion has started")


    # Lets check the Custom Excption we have created in exception.py

    try:
        data_ingestion = DataIngestion()
        train_data_path , test_data_path = data_ingestion.initiate_data_ingestion()


        data_transformation = DataTransformation()
        train_array , test_array , _ = data_transformation.initiate_data_transformation(train_data_path,test_data_path)  # It returns 3 things train_array ,test_array and  preprocessor.pkl where feature transformer was saved.
        # After this we must get a preprocessor.pkl file in artifacts folder.


        model_trainer = ModelTrainer()
        r2_score , model_name = model_trainer.initiate_model_trainer(train_array,test_array)
        logging.info(f"Best Model Name is:{model_name} and its r2_score is:{r2_score}")
        # After this we must get a model.pkl file in artifacts folder.


    except Exception as e:
        logging.info("Custom Exception Executed")
        raise CustomException(e,sys)
    
# Now lets execute it using python app.py in terminal...
