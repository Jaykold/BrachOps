import sys
from ujenkins import JenkinsError, JenkinsNotFoundError

def jenkins_error_detail(error, error_detail: Exception = None) -> str:
    _, _, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_num = exc_tb.tb_lineno

    if isinstance(error_detail, (JenkinsError, JenkinsNotFoundError)):
        jenkins_error = f"Jenkins API Error: {error_detail}"
    else:
        jenkins_error = str(error_detail) if error_detail else "Unknown error"

    error_message = f"Error occurred in {file_name} at line number {line_num}. {error}: {jenkins_error}"

    return error_message

class JenkinsCustomException(Exception):
    def __init__(self, error_message: str, error_detail: Exception = None):
        super().__init__(error_message)
        self.error_message = jenkins_error_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

# def error_message_detail(error, error_detail:Exception = None)->str:
#     _, _, exc_tb = error_detail.exc_info()
#     file_name = exc_tb.tb_frame.f_code.co_filename
#     line_num = exc_tb.tb_lineno

#     error_message = f"Error occurred in {file_name} at line number {line_num} error message {error}"

#     return error_message

# class CustomException(Exception):
#     def __init__(self, error_message: str, error_detail:Exception = None):
#         super().__init__(error_message)
#         self.error_message = error_message_detail(error_message, error_detail=error_detail)

#     def __str__(self):
#         return self.error_message

