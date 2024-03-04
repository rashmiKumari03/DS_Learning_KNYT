from src.student_performace_MLProject.pipelines.training_pipeline import run_training_pipeline
from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException

if __name__ == "__main__":
    try:
        logging.info("main_train.py serves as the entry point for running the training pipeline.")

        run_training_pipeline()
        
        logging.info("After Training Pipeline, our preprocessor and model are saved in pickle files.")
        logging.info("Now we will take incoming data and call the main_app.py file, triggering the Prediction Pipeline.")
        logging.info("Finally, after Training and Prediction Pipeline execution, we get our result as a prediction on the server.")
        
    except Exception as e:
        logging.error("An error occurred in main_train.py")
        raise CustomException(e)
