# Never modify these lines
import pymap
from colour import Color

# Step 1: Download a shapefile or geojson file from the internet
# and save it to the same folder as this file. Replace 'FILE NAME HERE.shp'
# with the name of the file.
# If it is a geojson file, replace from_shapefile with from_geojson.
#
# If you are using a shapefile, open the CSV file inside the shapefile
# and find the column number that contains the list of territories.
# Replace the 0 with this column number.
#
# Remember, when programming the first column is column 0.
#
# NOTE: NEVER USE EXCEL TO OPEN CSV FILES. Use Google Sheets instead.
#
# If you are having trouble with any of these steps, just experiment
# with different numbers instead of 0 to find one that gives
# the correct territory names.
#
# For geojson, open the geojson file, use ctrl-f to locate "properties",
# and replace the 0 with the property that contains the territory name.
# Don't forget quotation marks around the property name.
coords = pymap.from_shapefile('FILE NAME HERE.shp', 0)

# Step 2: Add the data
# Creates a spreadsheet for the data. Open it with Google Sheets.
# Create a second column with the data that you want to use for the map.
#
# Run only the code up through Line 33 by copying it into a new Python
# file.
coords.record_list_to_csv('FILE NAME HERE.csv')

# Once you have added all the data, load it.
# Make sure that this line and the previous line are never in the same file.
# Otherwise, your data will be overwritten by the previous line.
map_data = pymap.from_csv('FILE NAME HERE.csv')

# This line will always stay the same
svg_map = pymap.SVGMap(map_data, coords)

# Step 3: Add colors
# Replace the string at the end with the name of the column with the data in the spreadsheet.
svg_map['choropleth']['source'] = 'WHATEVER YOU NAMED THE COLUMN IN THE SPREADSHEET WITH YOUR DATA'

# The next two lines add colour. Copy them as many times as you like to create more colors.

# The line below creates a colour from hexadecimal.
# You can also load a colour from rgb by replacing hex_1='#HEXADECMIAL VALUE' with rgb(0, 0, 0)
# where the three 0's are placeholders for the r, g, and b values.
# Note that this is not standard rgb and each value must be between 0 and 1 (don't ask me why).
# That is why I recommend using hexadecimal.
my_colour = Color(hex_l='#HEXADECIMAL VALUE')

# Replace each string (between the '') with values associated with the colour.
# If the values are numeric, remove the quotation marks, otherwise, keep them.
# To allow for a range of values that all produce the same color,
# replace 'list' with 'range' and replace ['LIST', 'OF', 'ASSOCIATED', 'VALUES'] with [min, max]
# (with the minimum and maximum values that would result in the colour in place of min and max).
svg_map['choropleth'].add_colour(my_colour, ['LIST', 'OF', 'ASSOCIATED', 'VALUES'],'list')

# There is also a slightly more complicated usage that allows for a colour to be automatically determined.
# Let me know if you are interested in seeing an example usage for each.

# STEP 4: Load the map
# Change the value to False or remove the line if you are not ready to download the map.
# It is not recommended to download the map the first time you run it as you should make sure the map
# looks fine first.
svg_map['download'] = True

# Never modify this line
svg_map.save_to_file()

# Run the file and, after it finishes running, open index.html to see the completed map.
# If download is set to True, a png version will automatically be downloaded upon opening the file.
