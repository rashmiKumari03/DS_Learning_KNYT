# Here we will make a Custom Exception (We inherit the Exception)

import sys
from src.student_performace_MLProject.logger import logging

def error_message_detail(error):
    _, _, exc_tb = sys.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in Python script [{file_name}] at line number [{line_number}]: {error}"
    
    return error_message




class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)  # Since CustomException is inheriting Exception.
        

        # error_message_detail will be a function which will bring the error message.

        self.error_message = error_message_detail(error_message)

    def __str__(self):
        return self.error_message


# Now after this go to app.py and call it there and check whether it is woring fine of not.