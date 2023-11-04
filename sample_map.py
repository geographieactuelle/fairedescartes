import pymap
from colour import Color

# You may notice that there is an extra 1000 when compared to the template.
# This extra 1000 value overrides the default resolution.
# There is also an extra poly_keep = ['Rafah', 'North Gaza', 'Gaza', 'Khan Yunis', 'Deir Al Balah']
# The purpose of this is because in my example map I only want the regions of Palestine in Gaza.
# These two extra values are NOT necessary and the program will work just fine without them.

# Shapefile credit: geoBoundaries (https://www.geoboundaries.org)

coords = pymap.from_shapefile('https://github.com/geographieactuelle/fairedescartes/raw/main/geoboundaries-PSE-ADM2-all/geoBoundaries-PSE-ADM2.shp', 1, 1000, poly_keep=['Rafah', 'North Gaza', 'Gaza', 'Khan Yunis', 'Deir Al Balah'])

map_data = pymap.from_csv('sample_map.csv')

svg_map = pymap.SVGMap(map_data, coords)

svg_map['choropleth']['source'] = 'casualties'

# The lines below also differ slightly from the template.
# While minimum_colour and maximum_colour are similar to my_colour
# in the template, my_colour itself is different.

# This design is used to create a range of colours.
# The code will work perfectly fine even without this more complex usage
# If you are interested in learning about it, let me know.

minimum_colour = Color(rgb=(1,1,1))
maximum_colour = Color(rgb=(0.4,0,0))

my_colour = pymap.ChoroplethColourRange(minimum_colour, maximum_colour)

svg_map['choropleth'].add_colour(my_colour, [0, 3000], 'range')

# Also not in the template, but sets the width of the borders to 1.

svg_map['borders']['stroke-width'] = 1

svg_map['download'] = True

svg_map.save_to_file()
