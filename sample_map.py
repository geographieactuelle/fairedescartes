import pymap
from colour import Color

coords = pymap.from_shapefile('FILE_NAME.shp', 1, 1000)

coords.record_list_to_csv('sample_map.csv')

map_data = pymap.from_csv('sample_map.csv')
map_data['data'] = [1000 for _ in range(0, 100)]

svg_map = pymap.SVGMap(map_data, coords)

minimum_colour = Color(rgb=(1,1,1))
maximum_colour = Color(rgb=(0.4,0,0))

my_colour = pymap.ChoroplethColourRange(minimum_colour, maximum_colour)

svg_map['choropleth'].add_colour(my_colour, [0, 3000], 'range')

svg_map['borders']['stroke-width'] = 1

svg_map['download'] = True

svg_map.save_to_file()
