from __future__ import annotations
import shapefile
import json


class Coordinates(dict):

    def __init__(self, coords, records, zoom=1, translate=None, height=180, width=360):
        super().__init__()

        if translate is None:
            translate = [0, 0]

        self['data'] = coords
        self['metadata'] = {'scale': zoom, 'translate': translate, 'height': height, 'width': width}
        self['recordList'] = records

    def merge(self, coords: Coordinates) -> None:
        self['recordList'] = self['recordList'] + coords['recordList']
        self['data'] = self['data'] + coords['data']

    def modify_record(self, record: str | int, new: str) -> None:
        if type(record) == str:
            curr = None
            i = 0
            while not curr == record:
                curr = self['recordList'][i]
                i += 1
            self['recordList'][i] = new
            self['data'][i]['Country'] = new

        else:
            self['recordList'][record] = new
            self['data'][record]['Country'] = new


# Builds the MapData class
class MapData(dict):
    def __init__(self, data: dict, tlist='territory_list'):
        super().__init__()
        if type(data) is dict:
            self['data'] = data
            try:
                # Finds which list is the territory list and marks it
                self['territory_list'] = self['data'][tlist]
            except IndexError:
                raise IndexError('Territory list not found in data.')
        else:
            raise TypeError('Data must be a dictionary.')


# Builds the infobox class
class Infobox(dict):
    def __init__(self):
        # Sets style information
        super().__init__()
        self['style'] = {}
        self['style']['border'] = {}
        self['style']['border']['stroke-width'] = 3
        self['style']['border']['color'] = {}
        self['style']['border']['color']['r'] = 0
        self['style']['border']['color']['g'] = 0
        self['style']['border']['color']['b'] = 0
        self['style']['color'] = {}
        self['style']['color']['r'] = 255
        self['style']['color']['g'] = 255
        self['style']['color']['b'] = 255
        self['style']['text'] = []
        self['text'] = []

    # IMPORTANT: Text is based off of text containers that contain some text all formatted the same way.
    # There can be multiple text containers in a line. The text containers can contain text or data.
    def add_text(self, text: str, text_type='text', line=None, text_id=None,
                 font='Calibri', size=15, r=0, g=0, b=0) -> None:

        # Create text
        text_dict = {'type': text_type}
        # Assign unique ID
        if text_id is None:
            # Default ID is just a number, but a string
            text_dict['id'] = str(len(self['text']))
        else:
            # Custom ID
            text_dict['id'] = text_id

        # Decide which line text belongs on
        if line is None:
            if len(self['text']) == 0:
                # Text starts on first line
                text_dict['line'] = 0
            else:
                # Text continues on same line as before
                text_dict['line'] = self['text'][-1]['line']
        else:
            # Decide line manually
            text_dict['line'] = line

        text_dict['text'] = text

        # Create styles
        style_dict = {'font': font, 'size': size, 'r': r, 'g': g, 'b': b}

        # Add to object
        self['style']['text'].append(style_dict)
        self['text'].append(text_dict)

    def remove_text(self, text_id: int | str) -> None:
        if type(text_id) is int:
            del self['style']['text'][text_id]
            del self['text'][text_id]
        else:
            for text in self['text']:
                if text['id'] == text_id:
                    del self['style']['text'][self['text'].index(text)]
                    del self['text'][self['text'].index(text)]


class SVGMap(dict):
    def __init__(self, data=None, coords=None) -> None:
        super().__init__()
        self['map'] = coords
        self['choropleth'] = {}
        self['choropleth']['source'] = None
        self['choropleth']['colors'] = {}
        self['choropleth']['colors']['r'] = [0, 255]
        self['choropleth']['colors']['g'] = [0, 255]
        self['choropleth']['colors']['b'] = [0, 255]
        self['layers'] = []
        self['infobox'] = Infobox()

        # borders
        self['borders'] = {}
        self['borders']['colors'] = {}
        self['borders']['colors']['r'] = 0
        self['borders']['colors']['b'] = 0
        self['borders']['colors']['g'] = 0
        self['borders']['stroke-width'] = 3

        # background
        self['background_color'] = {}
        self['background_color']['r'] = 0
        self['background_color']['b'] = 0
        self['background_color']['g'] = 0

        # Supports two inputs: Hovering and clicking
        self['inputs'] = {}
        self['inputs']['onHover'] = ''
        self['inputs']['onMouseOut'] = ''
        self['inputs']['onClick'] = ''
        self['data'] = data

    def return_code(self) -> str:
        return 'var data = ' + json.dumps(self) + ';'

    def save_to_file(self, filename='autogenerated.js') -> None:
        code = self.return_code()
        file = open(filename, 'w')
        file.write(code)
        file.close()


def from_shapefile(file: str, record_id: int, res=5, isl=1, countries=None, zoom=1, translate=None, height=180,
                   width=360, extra_smooth=False) -> Coordinates:

    if countries is None:
        countries = []

    # Open shapefile with PySHP

    shp = shapefile.Reader(file)
    shapes = shp.shapes()
    # Define some variables
    svg = []
    record_list = []
    # Counter variable to track progress
    i = 0
    # Loop through each country or territory
    for country in shapes:
        i = i + 1
        # Restrict parsing to specific countries
        if (shp.shapeRecord(i - 1).record[record_id] in countries) or countries == []:
            # Track progress
            print(i)
            # Reset/define some variables
            main = []
            rounded = []
            # Loop through each point
            for point in country.points:
                # Find lat and long
                data = ','.join(str(x) for x in point)
                long = float(data.split(',')[0])
                lat = float(data.split(',')[1])
                # Convert to positive numbers
                long = long + 180
                lat = lat + 90
                # Convert original unrounded data to string
                data = str(long) + ',' + str(lat)
                data = data + ' '
                # Check if point appears twice. If so, it is a complete polygon
                if data in main:
                    main.append(data)
                    point_rounded = [str(round(long * res) / res), str(round(lat * res) / res)]
                    rounded.append(point_rounded)
                    
                    if len(rounded) > isl:
                        svg.append({'Points': rounded,
                                    'Country': shp.shapeRecord(i - 1).
                                    record[record_id].replace(' ', '')})
                    
                    main = []
                    rounded = []
                else:
                    # Round data as before and save the point
                    main.append(data)
                    rounded_data = [str(round(long * res) / res), str(round(lat * res) / res)]
                    if not rounded_data in rounded:
                        if (not extra_smooth) or len(rounded) == 0 or ((not rounded[-1][0] == rounded_data[0]) and (not rounded[-1][1] == rounded_data[1])):
                            rounded.append(rounded_data)
        record_list.append(shp.shapeRecord(i - 1).record[record_id].replace(' ', ''))
    # Create object from the points
    return Coordinates(svg, record_list, zoom, translate, height, width)