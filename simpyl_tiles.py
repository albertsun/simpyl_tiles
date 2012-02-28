import ctypes
from ctypes import *
from ctypes.util import find_lib


def bind_function(func, restype=None, argtypes=[]):
    if restype:
        func.restype = restype
    if argtypes:
        func.argtypes = argtypes
    return func

def status_output(func, argtypes=[]):
    return bind_function(func, c_void_p, argtypes)

# Make sure ctypes can find simple tiles
lib = ctypes.CDLL(find_lib("simple-tiles"))

map_new = bind_function(lib.simplet_map_new, c_void_p)
map_free = bind_function(lib.simplet_map_free, None, [c_void_p])

set_srs = status_output(lib.simplet_map_set_srs, [c_void_p, c_char_p])
get_srs = bind_function(lib.simplet_map_get_srs, None, [c_void_p, POINTER(c_char_p)])

set_size = status_output(lib.simplet_map_set_size, [c_void_p, c_uint, c_uint])
get_width = bind_function(lib.simplet_map_get_width, c_uint, [c_void_p])
get_height = bind_function(lib.simplet_map_get_height, c_uint, [c_void_p])
set_width = status_output(lib.simplet_map_set_width, [c_void_p, c_uint])
set_height = status_output(lib.simplet_map_set_height, [c_void_p, c_uint])
set_bounds = status_output(lib.simplet_map_set_bounds, [c_void_p, c_double, c_double, c_double, c_double])
set_slippy = status_output(lib.simplet_map_set_slippy, [c_void_p, c_uint, c_uint, c_uint])

set_bgcolor = status_output(lib.simplet_map_set_bgcolor, [c_void_p, c_char_p])
get_bgcolor = bind_function(lib.simplet_map_get_bgcolor, None, [c_void_p, POINTER(c_char_p)])

status_to_string = bind_function(lib.simplet_map_status_to_string, c_char_p, [c_void_p])


class Map:

    def __init__(self):
        self._map = c_void_p(map_new()) 


