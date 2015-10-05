# *-* coding:utf-8 *-*
# IBM Emulator function errors
import constants

class EmulatorError(Exception):
    """Base class for IBM emulator errors"""    
    # Each function has a list of possible errors. These dictionaries associate error codes and descriptions
    connect_error_list = {1:"An incorrect host presentation space ID was specified. The specified session either does not exist or is a logical printer session. This return code could also mean that the API Setting for DDE/EHLLAPI is not set on.", 
                4:"Successful connection was achieved, but the host presentation space is busy.", 
                5:"Successful connection was achieved, but the host presentation space is locked (input inhibited).",
                9:"A system error was encountered.",
                11:"This resource is unavailable. The host presentation space is already being used by another system function."}
    disconnect_error_list = {1:"Your program was not currently connected to the host presentation space.",
                9:"A system error was encountered."}
    send_key_error_list = {1:"Your program is not connected to a host session.",
                2:"An incorrect parameter was passed to EHLLAPI.",
                4:"The host session was busy; all of the keystrokes could not be sent.",
                5:"Input to the target session was inhibited or rejected; all of the keystrokes could not be sent.",
                9:"A system error was encountered."}
    query_cursor_error_list = {1:"Your program is not currently connected to a host session.",
                9:"A system error was encountered."}
    set_cursor_error_list = {1:"Your program is not connected to a host session.", 
                4:"The session is busy.", 
                7:"A cursor location less than 1 or greater than the size of the connected host presentation space was specified.",
                9:"A system error occurred."}
    get_text_error_list = {1:"Your program is not connected to a host session.",
                2:"An error was made in specifying parameters.",
                6:"The data to be copied and the target field are not the same size. The data is truncated if the string length is smaller than the field copied.",
                7:"The host presentation space position is not valid.",
                9:"A system error was encountered.",
                24:"Unformatted host presentation space."}

    # This dictionary associates each function code with an error list defined above.
    function_errors = {constants.CONNECT_PRESENTATION_SPACE:connect_error_list, 
              constants.DISCONNECT_PRESENTATION_SPACE:disconnect_error_list,
              constants.SEND_KEY:send_key_error_list, 
              constants.QUERY_CURSOR_LOCATION:query_cursor_error_list,
              constants.SET_CURSOR:set_cursor_error_list,
              constants.COPY_FIELD_TO_STRING:get_text_error_list}

    def __init__(self, func_num, return_code):
        self.error_case_list = self.function_errors[func_num] # returns a dictionary
        self.error_text = self.error_case_list[return_code] # selects a case from the error_case_list dictionary
    def __str__(self):
        return self.error_text