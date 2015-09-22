from ctypes import c_int, c_char_p, c_void_p, byref, WinDLL, WINFUNCTYPE

class Emulator(object):
    hllApi = None
    
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
        hllApiParams = (1, "_func_num", 0), (1, "_data_str", 0), (1, "_lenght",0), (1, "_ps_position",0)
        # Map the call ("HLLAPI(...)") to a Python name.
        self.hllApi = hllApiProto (("HLLAPI", hllDll), hllApiParams)
        
    def __enter__(self):
        self.connect_presentation_space()
    
    def __exit__(self, *args):
        self.disconnect_presentation_space()
    
    def connect_presentation_space(self):
        # Set up the variables and call the Python name with them.
        return self.hllApi (byref(self._func_num(1)), self._data_str("A"), byref(self._lenght(1)), byref(self._ps_position(0)))
    
    def disconnect_presentation_space(self):
        return self.hllApi (byref(self._func_num(2)), self._data_str("A"), byref(self._lenght(1)), byref(self._ps_position(0)))
        
    def sendpf23(self):
        return self.hllApi (byref(self._func_num(3)), self._data_str("@n"), byref(self._lenght(2)), byref(self._ps_position(0)))
        