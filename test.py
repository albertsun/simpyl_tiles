from simpyl_tiles import *

map = Map()
print map.set_srs("WGS84")
print map.status_to_string()
print map.get_srs()
del map

