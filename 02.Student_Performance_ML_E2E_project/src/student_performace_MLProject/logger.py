import logging
import os
from datetime import datetime


# Lets create a path where log files will get stored and name should looks like logs_datetime... so that we get the idea which is recent one.
LOG_FILE= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Make the path (currect location + logs + format_datetime)
log_path = os.path.join(os.getcwd(),"logs",LOG_FILE)

# Lets make the directory using this above address/location.
os.makedirs(log_path,exist_ok=True)


# Lets Save the logged information somewhere in a file in the created dir.
#Lets make the log_file with particular path:
LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

#Format of logged information must look like as follows:

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d   %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)



# Now once our logger.py is done...lets access this file from app.py ...
