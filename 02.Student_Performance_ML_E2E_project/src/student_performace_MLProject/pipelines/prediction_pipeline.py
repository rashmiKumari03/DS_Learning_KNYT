import os
import sys
import pandas as pd
from src.student_performace_MLProject.exception import CustomException
from src.student_performace_MLProject.utiles.utiles import load_object  #load_object just tto load the pickle file
from src.student_performace_MLProject.logger import logging


class PredictPipeline:
    def __init__(self):
        pass


    def predict(self,features):

        try:

            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")
            model_path=os.path.join("artifacts","model.pkl")

            model = load_object(file_path=model_path)   # We will take this load object from utiles we have creted there.
            preprocessor = load_object(file_path= preprocessor_path)

            # Now we need to transform the features
            data_transform = preprocessor.transform(features)
            logging.info(f"data_transform:{data_transform}")

            pred = model.predict(data_transform)
            logging.info(f"pred={pred}")
        except Exception as e:
            raise CustomException(e,sys)

        return pred

# Variable mapping function
# Creating CustomData : This will responsible for mapping all the inputs which where given by the form html to the backend with these particular values
class CustomData:
    def __init__(self,
         gender:str,
         race_ethnicity:str,
         parental_level_of_education:str,
         lunch:str,
         test_preparation_course:str,
         reading_score:float,
         writing_score:float):
          

        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch= lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score= reading_score
        self.writing_score=writing_score

    def get_data_as_DataFrame(self):
        try:
            custom_data_input_dict={
                
            "gender": [self.gender],
            "race_ethnicity": [self.race_ethnicity],
            "parental_level_of_education": [self.parental_level_of_education],
            "lunch":[self.lunch],
            "test_preparation_course":[self.test_preparation_course],
            "reading_score":[self.reading_score],
            "writing_score":[self.writing_score]

            }
            
            logging.info('Dataframe Gathered')

            return pd.DataFrame(custom_data_input_dict)   # We returned the dict as a dataframe...whatever input we recived from the html webpage.
     

        except Exception as e:
            raise CustomException(e,sys)





        

