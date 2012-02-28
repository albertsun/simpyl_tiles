import ctypes
from ctypes import *
from ctypes.util import find_library

# Make sure ctypes can find simple tiles
lib = ctypes.CDLL(find_library("simple-tiles"))

def bind_function(func, restype=None, argtypes=[]):
    if restype:
        func.restype = restype
    if argtypes:
        func.argtypes = argtypes

    def wrapper(*args):
        print args
        return func(*args[1:])
    return wrapper

def status_output(func, argtypes=[]):
    return bind_function(func, c_void_p, argtypes)

def str_ptr_output(func, restype=None, argtypes=[]):
    argtypes.append(POINTER(c_char_p))
    inner_func = bind_function(func, restype, argtypes)
    def wrapper(*args):
        a = c_char_p("")
        args += (a,)
        inner_func(*args)
        str_value = a.value
        lib.free(a)
        return str_value
    return wrapper
    

class Map:

    map_new = bind_function(lib.simplet_map_new, c_void_p)
    map_free = bind_function(lib.simplet_map_free, None, [c_void_p])

    set_srs = status_output(lib.simplet_map_set_srs, [c_void_p, c_char_p])
    get_srs = str_ptr_output(lib.simplet_map_get_srs, None, [c_void_p])

    set_size = status_output(lib.simplet_map_set_size, [c_void_p, c_uint, c_uint])
    get_width = bind_function(lib.simplet_map_get_width, c_uint, [c_void_p])
    get_height = bind_function(lib.simplet_map_get_height, c_uint, [c_void_p])
    set_width = status_output(lib.simplet_map_set_width, [c_void_p, c_uint])
    set_height = status_output(lib.simplet_map_set_height, [c_void_p, c_uint])
    set_bounds = status_output(lib.simplet_map_set_bounds, [c_void_p, c_double, c_double, c_double, c_double])
    set_slippy = status_output(lib.simplet_map_set_slippy, [c_void_p, c_uint, c_uint, c_uint])

    set_bgcolor = status_output(lib.simplet_map_set_bgcolor, [c_void_p, c_char_p])
    get_bgcolor = str_ptr_output(lib.simplet_map_get_bgcolor, None, [c_void_p])

    status_to_string = bind_function(lib.simplet_map_status_to_string, c_char_p, [c_void_p])

    def __init__(self):
        self._map = c_void_p(self.map_new()) 

    def __del__(self):
        self.map_free(self._map)

