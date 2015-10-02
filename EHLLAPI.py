# *-* coding: utf-8 *-*
import constants
from ctypes import c_int, c_char_p, c_void_p, byref, WinDLL, WINFUNCTYPE
from errors import EmulatorError
    
class Emulator(object):
    _hllApi = None
    def _func_num(self, arg):
        return c_int(arg)
    
    def _data_str(self, arg):
        return c_char_p(arg)
        
    def _lenght(self, arg):
        return c_int(arg)
    
    def _ps_position(self, arg):
        return c_int(arg)
        
    def __init__(self):
        # Load DLL.
        hllDll = WinDLL ("ehlapi32.dll")
        # Set up prototype and parameters for the desired function calls.
        hllApiProto = WINFUNCTYPE (c_int, c_void_p, c_void_p, c_void_p, c_void_p)
        hllApiParams = (1, "func_num", 0), (1, "data_str", 0), (1, "lenght", 0), (1, "ps_position", 0)
        # Map the call ("HLLAPI(...)") to a Python name.
        self._hllApi = hllApiProto (("HLLAPI", hllDll), hllApiParams)
        # Now each method sets up the variables and call the Python name with them.
    
    def hllApi(self, func_num, data_str, lenght, ps_position):
        return_value = self._hllApi(byref(func_num), data_str, byref(lenght), byref(ps_position))
        if return_value != 0:
            raise EmulatorError (func_num.value, return_value)
        return return_value
        
    def __enter__(self):
        self.connect()
    
    def __exit__(self, *args):
        self.disconnect()
    
    def connect(self, name="A"):
        if len(name) != 1 or not name.isalpha: raise ValueError("Argument name must be 1-character short name of the host presentation space")
        return self.hllApi (self._func_num(constants.CONNECT_PRESENTATION_SPACE), self._data_str(name), self._lenght(1), self._ps_position(0))
    
    def disconnect(self, name="A"):
        if len(name) != 1 or not name.isalpha: raise ValueError("Argument name must be 1-character short name of the host presentation space")
        return self.hllApi (self._func_num(constants.DISCONNECT_PRESENTATION_SPACE), self._data_str(name), self._lenght(1), self._ps_position(0))
        
    def send_keys(self, keys):
        # Cases:  the argument ''keys'' is just a regular string, it is a string inside <> or it is inside <> because it is a special command.
        # TODO: if it's not a command, use Copy String to Field (33) or Copy String to Presentation Space (15) to send string
        # TODO: split strings when len(keys) > 255     
        snd_txt = keys 
        txt_lenght = len(snd_txt)
        if snd_txt[0] == '<' and snd_txt[txt_lenght-1] == '>':
            try:
                snd_txt = constants.keyboard_mnemonics[keys.strip('<>').upper()] # Try to associate the string inside the <> with one object in the dictionary
                txt_lenght = len(snd_txt)
            except KeyError:
                snd_txt = keys # Couldn't find a match in the dictionary.   
        return self.hllApi (self._func_num(constants.SEND_KEY), self._data_str(snd_txt), self._lenght(txt_lenght), self._ps_position(0))
    
    def get_cursor(self):
        byte_pos = self._lenght(0) # byte_pos will be modified with the cursor position value
        self.hllApi (self._func_num(constants.QUERY_CURSOR_LOCATION), self._data_str(""), byte_pos, self._ps_position(0))
        return byte_pos.value
    
    def set_cursor(self, byte_pos):
        return self.hllApi (self._func_num(constants.SET_CURSOR), self._data_str(""), self._lenght(0), self._ps_position(byte_pos))