# *-* coding: utf-8 *-*
from ctypes import c_int, c_char_p, c_void_p, byref, WinDLL, WINFUNCTYPE

class Emulator(object):
       
    hllApi = None
    _last_func_num = None
    
    # ctypes conversion to avoid repetition inside other methods
    def _func_num(self, arg):
        self._last_func_num = arg
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
        
    def send_keys(self, keys):
        # Cases:  the argument ''keys'' is just a regular string, it is a string inside <> or it is inside <> because it is a special command.
        # TODO: handle return codes
        # TODO: if it's not a command, use Copy String to Field (33) or Copy String to Presentation Space (15) to send string
        # TODO: split strings when len(keys) > 255     
        snd_txt = keys 
        txt_lenght = len(snd_txt)
        keyboard_mnemonics = {'TAB':'@T', 'ENTER':'@E', 'ERASEEOF':'@F', 'BACKSPACE':'@<', 'BACKTAB':'@B', 'CLEAR':'@C', 'DOWN':'@V', 'LEFT':'@L', 'RIGHT':'@Z', 'CURSEL':'@A@J', 'UP':'@U', 'DELETE':'@D', 'PF1':'@1', 'PF2':'@2', 'PF3':'@3', 'PF4':'@4', 'PF5':'@5', 'PF6':'@6', 'PF7':'@7', 'PF8':'@8', 'PF9':'@9', 'PF10':'@a', 'PF11':'@b', 'PF12':'@c', 'PF13':'@d', 'PF14':'@e', 'PF15':'@f', 'PF16':'@g', 'PF17':'@h', 'PF18':'@i', 'PF19':'@j', 'PF20':'@k', 'PF21':'@l', 'PF22':'@m', 'PF23':'@n', 'PF24':'@o', 'PA1':'@x', 'PA2':'@y', 'PA3':'@z', 'PAGEUP':'@u', 'PAGEDN':'@v', 'RESET':'@R', 'SYSREQ':'@A@H', 'HELP':'@H', 'HOME':'@0', 'INSERT':'@I', 'NEWLINE':'@N', 'DUP':'@S@x', 'ERINP':'@A@F', 'FLDEXT':'@A@E', 'FIELDMARK':'@S@y', 'FIELD-':'@A@-', 'FIELD+':'@A@+'}
        if snd_txt[0] == '<' and snd_txt[txt_lenght-1] == '>':
            try:
                snd_txt = keyboard_mnemonics[keys.strip('<>')] # Try to associate the string inside the <> with one object in the dictionary
                txt_lenght = len(snd_txt)
            except KeyError:
                snd_txt = keys # Couldn't find a match in the dictionary.   
        return self.hllApi (byref(self._func_num(3)), self._data_str(snd_txt), byref(self._lenght(txt_lenght)), byref(self._ps_position(0)))
    
    def get_cursor(self):
            pos = self._lenght(0)
            self.hllApi (byref(self._func_num(7)), self._data_str(""), byref(pos), byref(self._ps_position(0)))
            return pos
    # TODO: 
    # def getconnectionstatus
    # def cursorcoordconversion
    # def getcursorposition
    # def setcursorposition
        
