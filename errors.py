# *-* coding:utf-8 *-*
# IBM Emulator function errors
import constants

class EmulatorError(Exception):
    """Base class for IBM emulator errors"""    
    # Each function has a list of possible errors. These dictionaries associate error codes and descriptions
    query_cursor_error_list = {1:"Your program is not currently connected to a host session.", 9:"A system error was encountered."}
    connect_error_list = {1:"An incorrect host presentation space ID was specified. The specified session either does not exist or is a logical printer session. This return code could also mean that the API Setting for DDE/EHLLAPI is not set on.", 4:"Successful connection was achieved, but the host presentation space is busy.", 5:"Successful connection was achieved, but the host presentation space is locked (input inhibited).", 9:"A system error was encountered.", 11:"This resource is unavailable. The host presentation space is already being used by another system function."}
    # This dictionary associates each function code with an error list defined above.
    function_errors = {1:connect_error_list, 7:query_cursor_error_list}

    def __init__(self, func_num, return_code):
        self.error_case_list = self.function_errors[func_num] # returns a dictionary
        self.error_text = self.error_case_list[return_code] # selects a case from the error_case_list dictionary
    def __str__(self):
        return self.error_text