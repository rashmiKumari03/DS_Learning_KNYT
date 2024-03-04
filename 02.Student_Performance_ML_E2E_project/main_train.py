from src.student_performace_MLProject.pipelines.training_pipeline import run_training_pipeline
from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException

import sys

if __name__ == "__main__":
    try:
          logging.info("main_train.py serves as the entry point for running the training pipeline.")

          run_training_pipeline()
          
          logging.info("After Training_Pipeline our preprocessor and model got saved in pickle files.")
          logging.info("Now we will take incoming data , and Call the main_app.py file ..so that PredictionPipeline will get triggered.")
          logging.info("Finally After Training and Prediction Pipeline execution we got our result as prediction on the server.")
          

    except Exception as e:
        raise CustomException(e,sys)
  