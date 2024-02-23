import os
from pathlib import Path
import logging 

logging.basicConfig(level=logging.INFO)

project_name = 'student_performace_MLProject'


list_of_files=[
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/components/model_monitoring.py",

    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/pipelines/training_pipeline.py",
    f"src/{project_name}/pipelines/prediction_pipeline.py",

    f"src/{project_name}/utiles/__init__.py",
    f"src/{project_name}/utiles/utiles.py",
    
    f"src/{project_name}/exception.py",
    f"src/{project_name}/logger.py",
    "app.py",
    "requirements.txt",
    "setup.py"

]



# Now code will execute these above paths and make directories.

for filepath in list_of_files:
    filepath = Path(filepath)  # We are converting the string to actual path using Path
    filedir , filename = os.path.split(filepath)  

    # If file dir is not equal to "" ie. if file dir is non empty...means there is something in filedir then make the dir with that address/path.

    if filedir != "":
        os.makedirs(filedir,exist_ok=True) 
        logging.info(f"Creating directory:{filedir} for the file {filename}")
    
    # if that above path doesnot exist or path size is zero ==> path doesnot exist...then we will create an empty filepath..else filename already exist.
    # Suppose we already have setup.py and requirements.txt whose size is non zero therefore it will skip the if part and comes to else and prints file already exist.
        
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file:{filepath}")
    else:
        logging.info(f"{filename} is already exists")


# Run it in terminal : python template.py