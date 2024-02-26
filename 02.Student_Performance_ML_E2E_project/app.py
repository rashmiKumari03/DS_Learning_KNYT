# We know the location of logger.py so lets call it from there.
import sys
from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException

from src.student_performace_MLProject.components.data_ingestion import DataIngestion

# To check whether things are working file...lets make it.
if __name__ == "__main__":
    logging.info("The Exectuion has started")


    # Lets check the Custom Excption we have created in exception.py

    try:
        # Step 1: DataIngestion 
       
        data_ingestion=DataIngestion()
        data_ingestion.initiate_data_ingestion()


    except Exception as e:
        logging.info("Custom Exception Executed")
        raise CustomException(e,sys)
    
# Now lets execute it using python app.py in terminal...
