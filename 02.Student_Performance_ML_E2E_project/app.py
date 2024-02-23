# We know the location of logger.py so lets call it from there.

from src.student_performace_MLProject.logger import logging


# To check whether things are working file...lets make it.
if __name__ == "__main__":
    logging.info("The Exectuion has started")

# Now lets execute it using python app.py in terminal...
