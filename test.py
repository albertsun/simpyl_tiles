from simpyl_tiles import *

map = Map()
print map.set_srs(map._map, "WGS84")
print map.status_to_string(map._map)
print map.get_srs(map._map)
del map

