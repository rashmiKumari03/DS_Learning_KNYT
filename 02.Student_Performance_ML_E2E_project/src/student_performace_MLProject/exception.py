# Here we will make a Custom Exception (We inherit the Exception)

import sys
from src.student_performace_MLProject.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message





class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message) # Since CustomException is inheriting Exception.
        self.error_message=error_message_detail(error_message,error_details)

    def __str__(self):
        return self.error_message  # error_message_detail will be a function which will bring the error message.


# Now after this go to app.py and call it there and check whether it is woring fine of not.