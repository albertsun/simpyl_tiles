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

def simplet_class_method(func):
    @wraps(func)
    def wrapper(*args):
        args = list(args)
        args[0] = args[0]._simplet_ptr
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
    """
    Wraps a Simple Tiles simplet_map_t object.
    """
    __map_new = bind_function(lib.simplet_map_new, c_void_p)
    __map_free = bind_function(lib.simplet_map_free, None, [c_void_p])

    set_srs = simplet_class_method(status_output(lib.simplet_map_set_srs, [c_void_p, c_char_p]))
    get_srs = simplet_class_method(str_ptr_output(lib.simplet_map_get_srs, None, [c_void_p]))

    set_size = simplet_class_method(status_output(lib.simplet_map_set_size, [c_void_p, c_uint, c_uint]))
    get_width = simplet_class_method(bind_function(lib.simplet_map_get_width, c_uint, [c_void_p]))
    get_height = simplet_class_method(bind_function(lib.simplet_map_get_height, c_uint, [c_void_p]))
    set_width = simplet_class_method(status_output(lib.simplet_map_set_width, [c_void_p, c_uint]))
    set_height = simplet_class_method(status_output(lib.simplet_map_set_height, [c_void_p, c_uint]))
    set_bounds = simplet_class_method(status_output(lib.simplet_map_set_bounds, [c_void_p, c_double, c_double, c_double, c_double]))
    set_slippy = simplet_class_method(status_output(lib.simplet_map_set_slippy, [c_void_p, c_uint, c_uint, c_uint]))

    set_bgcolor = simplet_class_method(status_output(lib.simplet_map_set_bgcolor, [c_void_p, c_char_p]))
    get_bgcolor = simplet_class_method(str_ptr_output(lib.simplet_map_get_bgcolor, None, [c_void_p]))

    __add_layer = simplet_class_method(bind_function(lib.simplet_map_add_layer, c_void_p, [c_void_p, c_char_p]))
    def add_layer(self, datastring):
        lyr_ptr = c_void_p(self.__add_layer(datastring))
        lyr = Layer(ptr=lyr_ptr)
        self.layers.append(lyr)
        return lyr

    __add_layer_directly = simplet_class_method(bind_function(lib.simplet_map_add_layer_directly, c_void_p, [c_void_p, c_void_p]))
    def add_layer_directly(self, layer):
        lyr_ptr = c_void_p(self.__add_layer_directly(layer._simplet_ptr))
        self.layers.append(layer)
        return layer

    get_status = simplet_class_method(status_output(lib.simplet_map_get_status, [c_void_p]))
    status_to_string = simplet_class_method(bind_function(lib.simplet_map_status_to_string, c_char_p, [c_void_p]))
    is_valid = simplet_class_method(status_output(lib.simplet_map_is_valid, [c_void_p]))

    render_to_png = simplet_class_method(bind_function(lib.simplet_map_render_to_png, None, [c_void_p, c_char_p]))

    set_buffer = simplet_class_method(bind_function(lib.simplet_map_set_buffer, None, [c_void_p, c_double]))
    get_buffer = simplet_class_method(bind_function(lib.simplet_map_get_buffer, c_double, [c_void_p]))

    def __init__(self):
        self._simplet_ptr = c_void_p(self.__map_new()) 
        self.layers = []

    def __del__(self):
        self.__map_free(self._simplet_ptr)

class Bounds:

    __bounds_new = bind_function(lib.simplet_bounds_new, c_void_p)
    __bounds_free = bind_function(lib.simplet_bounds_free, None, [c_void_p])

    to_wkt = simplet_class_method(str_ptr_output(lib.simplet_bounds_to_wkt, c_void_p, [c_void_p]))

    def __init__(self):
        self._simplet_ptr = c_void_p(self.__bounds_new())

    def __del__(self):
        self.__bounds_new(self._simplet_ptr)

class Layer:
    
    __layer_new = bind_function(lib.simplet_layer_new, c_void_p, [c_char_p])
    __layer_free = bind_function(lib.simplet_layer_free, None, [c_void_p])

    set_source = simplet_class_method(bind_function(lib.simplet_layer_set_source, None, [c_void_p,c_char_p]))
    get_source = simplet_class_method(str_ptr_output(lib.simplet_layer_get_source, None, [c_void_p]))

    __add_query = simplet_class_method(bind_function(lib.simplet_layer_add_query, c_void_p, [c_void_p, c_char_p]))
    def add_query(self, ogrsql):
        query_ptr = c_void_p(self.__add_query(ogrsql))
        query = Query(ptr=query_ptr)
        self.queries.append(query)
        return query

    __add_query_directly = simplet_class_method(bind_function(lib.simplet_layer_add_query_directly, c_void_p, [c_void_p, c_void_p]))
    def add_query_directly(self, query):
        query_ptr = c_void_p(self.__add_query_directly(query._simplet_ptr))
        self.queries.append(query)
        return query

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("ptr"):
            self._simplet_ptr = kwargs.get("ptr")
        elif kwargs.has_key("datastring"):
            self._simplet_ptr = c_void_p(self.__layer_new(kwargs.get("datastring")))

        self.queries = []

    def __del__(self):
        self.__layer_free(self._simplet_ptr)

class Query:

    __query_new = bind_function(lib.simplet_query_new, c_void_p, [c_char_p])
    __query_free = bind_function(lib.simplet_query_free, None, [c_void_p])

    set = simplet_class_method(bind_function(lib.simplet_query_set, None, [c_void_p, c_char_p]))
    get = simplet_class_method(str_ptr_output(lib.simplet_query_get, None, [c_void_p]))

    __add_style = simplet_class_method(bind_function(lib.simplet_query_add_style, c_void_p, [c_void_p, c_char_p, c_char_p]))
    def add_style(self, key, arg):
        style_ptr = c_void_p(self.__add_style(key, arg))
        style = Style(ptr=style_ptr)
        self.styles.append(style)
        return style

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("ptr"):
            self._simplet_ptr = kwargs.get("ptr")
        elif kwargs.has_key("sqlquery"):
            self._simplet_ptr = c_void_p(self.__query_new(kwargs.get("sqlquery")))

        self.styles = []

    def __del__(self):
        self.__query_free(self._simplet_ptr)

class Style:

    __style_new = bind_function(lib.simplet_style_new, c_void_p, [c_char_p, c_char_p])
    __style_free = bind_function(lib.simplet_style_free, None, [c_void_p])

    set_key = simplet_class_method(bind_function(lib.simplet_style_set_key, None, [c_void_p,c_char_p]))
    set_arg = simplet_class_method(bind_function(lib.simplet_style_set_arg, None, [c_void_p,c_char_p]))
    get_key = simplet_class_method(str_ptr_output(lib.simplet_style_get_key, None, [c_void_p]))
    get_arg = simplet_class_method(str_ptr_output(lib.simplet_style_get_arg, None, [c_void_p]))

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("ptr"):
            self._simplet_ptr = kwargs.get("ptr")
        elif kwargs.has_key("key") and kwargs.has_key("arg"):
            self._simplet_ptr = c_void_p(self.__style_new(kwargs.get("key"), kwargs.get("arg")))

    def __del__(self):
        self.__query_free(self._simplet_ptr)

