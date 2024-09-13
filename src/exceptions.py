import sys
from src import logger

def error_message_detail(error, error_detail: sys):
    """
    Custom error handler to display the error message, 
    the line where the error occurred, and the file name.

    Args:
        error (Exception): The exception that was raised.
        error_detail (sys): The sys module to extract error details.

    Returns: 
        str: Custom error message containing file name, line number, and error message.
    """
    _, _, exc_traceback = error_detail.exc_info()  # Retrieves exception type, value, and traceback.
    
    # Extract file name and line number from traceback.
    file_name = exc_traceback.tb_frame.f_code.co_filename
    line_number = exc_traceback.tb_lineno
    error_message = (
        f"Error occurred in python script: {file_name.split('/')[-1]} \n"
        f"Line number: {line_number} \n"
        f"Error message: {str(error)}"
    )

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message) 
        self.error_message = error_message_detail(error_message, error_detail=error_detail)  
        
    def __str__(self):
        return self.error_message 
    
    
# To test the code above
# if __name__ == '__main__':
#     try:
#         a = 1/0
#     except Exception as e:
#         logger.logging.info("Division by Zero")
#         raise CustomException(e, sys)