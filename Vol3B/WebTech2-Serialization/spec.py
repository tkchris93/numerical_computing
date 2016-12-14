#serialization.py
'''Volume 3B: Web Technologies 2 - Serialization
<Name>
<Class>
<Date>
'''

import json
import datetime

# Problem 1
class DateEncoder(json.JSONEncoder):
    '''
    This is a class shell for the datetime object
    encoder. See example in Lab PDF for more
    information.
    '''
    

def date_decoder(dct):
    '''
    This method should be used to decode a
    datetime object from JSON format to Python.
    See Lab PDF for more information.
    '''
    def dedate(s):
        # Put information here.
    
    # Try to decode any value that looks like a date
    for i, k in dct.iteritems():
        try:
            dct[i] = dedate(k)
        except:
            continue
    return dct
    
# Problem 2
def water_data():
    '''
    This method should get a JSON file from 
    https://data.lacity.org/resource/v87k-wgde.json
    using the requests library. It should then
    show a scatter plot of the water usage from
    2012 to 2013 organized by latitude and longitude.
    
    Scatter Plot:
    x-axis: longitude
    y-axis: latitude
    point size: water use (hundreds of cubic feet)
    '''
    
    
# Problem 3
def books_xml():
    '''
    This method should include all code used to 
    find:
    - The author of the most expensive book
    - How many books were published before May 1,
    2000
    - Which books reference Microsoft in their 
    description
    
    in books.xml
    ''' 
