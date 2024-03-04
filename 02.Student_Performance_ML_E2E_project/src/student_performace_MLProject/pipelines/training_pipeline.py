import sys
from src.student_performace_MLProject.logger import logging
from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.components.data_ingestion import DataIngestion
from src.student_performace_MLProject.components.data_transformation import DataTransformation
from src.student_performace_MLProject.components.model_trainer import ModelTrainer
import warnings

warnings.filterwarnings('ignore')

def run_training_pipeline():
    """
    Run the training pipeline.

    This function initiates data ingestion, transformation, and model training.
    """

    logging.info("Training Pipeline Has Started!!!!")
    try:
        logging.info("The Execution has started")

        data_ingestion = DataIngestion()
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

        data_transformation = DataTransformation()
        train_array, test_array, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)

        model_trainer = ModelTrainer()
        r2_score, model_name = model_trainer.initiate_model_trainer(train_array, test_array)

        logging.info(f"Best Model Name is: {model_name} and its r2_score is: {r2_score}")

    except Exception as e:
        logging.error("Error occurred during training pipeline execution")
        raise CustomException(e)

