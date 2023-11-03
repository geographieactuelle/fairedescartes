# Introduction


This is a library to make an interactive Javascript-based SVG map within minutes. It can make a choropleth map from a Shapefile or geojson file, add an infobox to the map, change map data, and more.

If you do not have programming experience, please read the instructions in the template in example.py


## Requirements

The PySHP library is required in order for the library to work. A shapefile of the region to be mapped is also required. Also, adding data is also required.

## Basic concepts

All classes are based off dictionaries so it can be easily converted to JSON. The main classes are the Infobox class, the SVGMap class, the Coordinates class, and the MapData class.

# Coordinates class

## Creating a Coordinates object directly

This is possible but not recommended.

### Parameters

#### coords

A list of dictionaries containing the coordinates, equivalent to `['data']` in the dictionary (see below)

#### records

A list of all the records associated with each shape.

#### zoom, translate, height, and width

See below

## from_shapefile() and from_geojson(): Create a Coordinates object from a shapefile or geojson file

Shapefiles are read based on the PySHP library and then converted to a format that can be used to make an SVG map. Use the Coordinates class to load a map. Numbers will be printed showing the progress loading as it may take a while.
### Parameters

The only required parameters are the file and the recordId. There are also many optional parameters.

#### file

The location of the file to be read.

#### record_id

In a shapefile: The column number of the shape record that will serve as the name of each polygon. Columns start at 0. This will be used to match shapes with data. Only one is permitted.

In a geojson file: The name of the property that will serve as the name of each polygon.

#### res

The resolution. By default this is 10, meaning that points are rounded to 1/10 of a unit of latitude and longitude. Lower resolutions load faster but higher are more accurate.

#### isl

Used to exclude small islands or shapes. By default only shapes with a single coordinate are excluded. This value is an integer corresponding to the highest number of coordinates a shape could have and be excluded.

#### poly_keep

Chooses which shapes to include based on shape records. Takes a list. Leaving blank or entering a blank list will include all shapes or countries.

#### zoom

This chooses what proportion of the map should be shown. It is by default None. For example, if it is 2 it will show only half of the latitude values and half of the longitude values so only 1/4 of the map. If it is None, it will zoom automatically based on the coordinates of the shapes involved.

#### translate

After zooming in, allows choosing which part of the map to see. Accepts a list of two values that correspond to the coordinates for the bottom-left corner that should be shown. Note that these are always positive, so for the latitude add 90 and the longitude add 180. Longitude comes first. It is by default None. If it is None, it will translate automatically based on the coordinates of the shapes involved.

#### height

The height of the map, 180 by default

#### width

The width of the map, 360 by default

#### relative_zoom

Only affects the map if `zoom is None`. Note that higher numbers correspond to zooming out. Affects the zoom relative to the automatically-generated zoom level. By default 1.1.

#### extra_smooth

Makes the map lower resolution, slightly smoother. By default false. Feature only available for from_shapefile(), not for from_geojson()

## Understanding the dictionary

`['data']` lists all the shapes

`['data'][32]['Points']` lists the points of the 33rd shape.

`['data'][32]['Points'][64][0]` is the longitude of the 65th point of the 33rd shape.

`['data'][32]['Points'][64][1]` is the latitude of the 65th point of the 33rd shape.

`['data'][32]['Country']` is the Shape Record of the 33rd shape. Spaces are removed.

`['metadata']['scale']` is the zoom parameter.

`['metadata']['translate']` is the translate parameter.

`['metadata']['height']` is the height parameter.

`['metadata']['width']` is the width parameter.

`['recordList']` is a list of all the shape records used. Spaces are removed.

These can all be modified at any time.

## merge()

Merges with another Coordinates object

### Parameters

#### coords

A second Coordinates object

## modify_record()

Modifies a record in both the record list and in the list of points.

### Parameters

#### record

If this is an integer, it is the index of the record to be modified, if it is a string, it is the record itself.

#### new

The new value for the record.

# Importing data

The MapData class is responsible for managing data. The only two parameters are the dictionary with the data and the territory list.

## Using the MapData() initializer

### Parameters

#### data

Must be a dictionary containing several lists of data. (The keys should be strings.)

#### tlist

The name of the key corresponding to the list of territories in the data. By default 'territory_list'.

## from_csv()

Imports data from a csv file.

### Parameters

#### location

The location of the file

#### territory_list

The column number of the territory list. By default 0.

## The territory list

The parameter tlist is by default territory_list. This shows which list is the list of territories that correspond to the shape records in the shapefile. They do not have to be in the same order.

## Understanding the dictionary

`['data']` is the original dictionary.

`['territory_list']` is the list of territories. It is still located in the original dictionary but also additionally located here.

# Making an infobox

The Infobox class has no parameters.

## Adding text

Use the addText() method. This does have many parameters.

### The text parameter

This parameter is the text itself.

### Adding a formula based on data

Repace the text with a formula in the format `data["data"]["data"][DATASET][c]`, whare DATASET should be replaced with the list name from the MapData class that you wish to access and c is the territory the infobox is for. Of course c will vary, so just leave it as `c` in the formula. Any javascript formula will work.

Next, add the optional parameter `textType = 'formula'` to show it is a formula.

### The line parameter

Specifies which line of the infobox it should appear on, starting with line 0. By default it uses the line of the previous text added. (If the previous text is removed it will not be adjusted.)

### textId

Assigns a unique ID to each section of text. By default it is simply a number (although a string).

### font, size, r, g, and b

r, g, and b determine the color. They are by default all 0.

font determines the font. By default calibri.

size determines the font size. By default 15.

## Removing text

Removes text. Only parameter is the textId. If it is an integer it will delete that list item from the list of text, which doesn't always correspond to the default textId number.

## Understanding the dictionary

`['style']['border']['stroke-width']` is the width of the border of the infobox.

`['style']['border']['color']['r']` is the red in the border color. Same applies with green and blue.

`['style']['color']` is the fill color. It works the same way as the border color.

`['style']['text']` is a list with style information for each piece of text. The list contains a style dictionary for each piece of text with items based on the parameters in the addText function.

`['text']` is a dictionary a lot like `['style']['text']` but contains the text itself `['text']['text']`, the textId `['text']['id']`, and whether it is `text` or a 	`formula` `['text']['type']`.

# Putting it all together

## Creating an SVGMap object

Requires two parameters: a MapData object and a Coordinates object.

### Adding an infobox

Use `['infobox'] = infobox_object`

## Coloring the map

Use `['choropleth']['source']` to denote the list name containing the data to color the map.

### Choosing colors

Use `['choropleth']['colors']['r']` for the red. Green and blue are chosen similarly. This should be a list with only two items: The first the red at the lowest point in the dataset and the second the red at the highest.

## Making it interactive

Three inputs are supported:

`['inputs']['onMouseOut']`

`['inputs']['onHover']`

`['inputs']['onClick']`

This should be Javascript code.

### Accessing shape-specific information

`[COUNTRY]` will be replaced with the index of the country in the territory_list.

### Showing and hiding the infobox
Use `showInfobox([COUNTRY]);` and `hideInfobox([COUNTRY]);` to show and hide the infobox.

### Reloading and recoloring the map
Use `loadMap();` to completely reload the map.

Use `colorMap();` to just re-color the map.

This is useful if inputs result in changing the data.

---
All of the functions above can be accessed through external scripts.

---

# Saving and loading the map

The SVGMap class has a `returnCode()` method that returns javascript code for loading the map.

## Loading the map

Use the accompanying HTML and Javascript file to load the map.
