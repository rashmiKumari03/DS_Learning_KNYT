# We know the location of logger.py so lets call it from there.
import sys
from src.student_performace_MLProject.logger import logging

from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.components.data_ingestion import DataIngestion
from src.student_performace_MLProject.components.data_transformation import DataTransformation

# To check whether things are working file...lets make it.
if __name__ == "__main__":
    logging.info("The Exectuion has started")


    # Lets check the Custom Excption we have created in exception.py

    try:
        data_ingestion = DataIngestion()
        train_data_path , test_data_path = data_ingestion.initiate_data_ingestion()


        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path,test_data_path)




    except Exception as e:
        logging.info("Custom Exception Executed")
        raise CustomException(e,sys)
    
# Now lets execute it using python app.py in terminal...
