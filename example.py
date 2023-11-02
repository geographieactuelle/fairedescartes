# Never modify these lines
import pymap
from colour import Color

# Replace the 0 with whichever number contains the names of the territories.
coords = pymap.from_shapefile('FILE NAME HERE.shp', 0)

# Use either from_shapefile or from_geojson, not both.
coords = pymap.from_geojson('FILE NAME HERE.shp', 'RECORD NAME')

# Creates a spreadsheet for the data.
coords.record_list_to_csv('FILE NAME HERE.csv')

# Run this line only after adding the data.
map_data = pymap.from_csv('FILE NAME HERE.csv')

# This line will always stay the same
svg_map = pymap.SVGMap(map_data, coords)

# Tells the program where your data is
svg_map['choropleth']['source'] = 'WHATEVER YOU NAMED THE COLUMN IN THE SPREADSHEET WITH YOUR DATA'

# Lines 23-39 add colour. Use this as many times as you need.

# The line below creates a colour from hexadecimal.
my_colour = Color(hex_l='#HEXADECIMAL VALUE')

# Adds color from rgb. Use either this or the statement above, not both.
# Note that each value must be between 0 and 1, not between 0 and 255 like in standard rgb.
my_colour = Color(rgb=(0, 0, 0))

# List the data values that could result in such a colour on the map
svg_map['choropleth'].add_colour(my_colour, ['LIST', 'OF', 'ASSOCIATED', 'VALUES'])

# Lists a range of data values that could result in such a colour on the map.
# Use either this or the statement above, not both. Replace 0 with the minimum and 100 with the maximum.
svg_map['choropleth'].add_colour(my_colour, [0, 100], 'range')

# There is also a slightly more complicated usage that allows for a colour to be automatically determined.
# Let me know if you are interested in seeing an example usage for each.

# Change the value to False or remove the line if you are not ready to download the map.
svg_map['download'] = True

# Never modify this line
svg_map.save_to_file()
