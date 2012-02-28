import ctypes
from ctypes import *
from ctypes.util import find_library

from functools import wraps

# Make sure ctypes can find simple tiles
lib = ctypes.CDLL(find_library("simple-tiles"))

def bind_function(func, restype=None, argtypes=[]):
    if restype:
        func.restype = restype
    if argtypes:
        func.argtypes = argtypes
    return func

def map_function(func):
    @wraps(func)
    def wrapper(*args):
        args = list(args)
        args[0] = args[0]._map
        return func(*args)
    return wrapper

def status_output(func, argtypes=[]):
    return bind_function(func, c_void_p, argtypes)

def str_ptr_output(func, restype=None, argtypes=[]):
    argtypes.append(POINTER(c_char_p))
    inner_func = bind_function(func, restype, argtypes)
    @wraps(inner_func)
    def wrapper(*args):
        a = c_char_p("")
        args += (a,)
        inner_func(*args)
        str_value = a.value
        lib.free(a)
        return str_value
    return wrapper
    

class Map:


    __map_new = bind_function(lib.simplet_map_new, c_void_p)
    __map_free = bind_function(lib.simplet_map_free, None, [c_void_p])

    set_srs = map_function(status_output(lib.simplet_map_set_srs, [c_void_p, c_char_p]))
    get_srs = map_function(str_ptr_output(lib.simplet_map_get_srs, None, [c_void_p]))

    set_size = map_function(status_output(lib.simplet_map_set_size, [c_void_p, c_uint, c_uint]))
    get_width = map_function(bind_function(lib.simplet_map_get_width, c_uint, [c_void_p]))
    get_height = map_function(bind_function(lib.simplet_map_get_height, c_uint, [c_void_p]))
    set_width = map_function(status_output(lib.simplet_map_set_width, [c_void_p, c_uint]))
    set_height = map_function(status_output(lib.simplet_map_set_height, [c_void_p, c_uint]))
    set_bounds = map_function(status_output(lib.simplet_map_set_bounds, [c_void_p, c_double, c_double, c_double, c_double]))
    set_slippy = map_function(status_output(lib.simplet_map_set_slippy, [c_void_p, c_uint, c_uint, c_uint]))

    set_bgcolor = map_function(status_output(lib.simplet_map_set_bgcolor, [c_void_p, c_char_p]))
    get_bgcolor = map_function(str_ptr_output(lib.simplet_map_get_bgcolor, None, [c_void_p]))

    status_to_string = map_function(bind_function(lib.simplet_map_status_to_string, c_char_p, [c_void_p]))

    def __init__(self):
        self._map = c_void_p(self.__map_new()) 

    def __del__(self):
        self.__map_free(self._map)

