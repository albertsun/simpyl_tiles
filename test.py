from simpyl_tiles import *

m = Map()
m.set_slippy(0,0,0)
m.set_size(1000,1000)
m.set_bgcolor("#ddeeff")
layer = m.add_layer("data/ne_10m_admin_0_countries.shp")
query = layer.add_query("SELECT * from 'ne_10m_admin_0_countries'")
query.add_style("stroke", "#226688")
query.add_style("line-join", "round")
query.add_style("weight", "3")

query2 = layer.add_query("SELECT * from 'ne_10m_admin_0_countries'")
query2.add_style("weight", "0.5")
query2.add_style("fill", "#d3e46f")
query2.add_style("stroke", "#ffffff")
query2.add_style("line-join", "round")

query2.add_style("text-field", "NAME")
query2.add_style("font", "Lucida Grande, Regular 8")
query2.add_style("color", "#444444ff")
query2.add_style("text-stroke-color", "#ffffffcc")
query2.add_style("text-stroke-weight", "2")
query2.add_style("letter-spacing", "1")

if m.is_valid():
    m.render_to_png("out.png")
    print "done rendering"

