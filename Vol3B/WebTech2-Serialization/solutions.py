import json
import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt

# Problem 1

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def date_decoder(dct):
    def dedate(s):
        # Ignore the quote marks (we have a string inside a string)
        parts = s[1:-1].split('.')
        r = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
        if parts[1]:
            r.replace(microsecond=int(parts[1]))
        return r
    
    # Try to decode any value that looks like a date
    for i, k in dct.iteritems():
        try:
            dct[i] = dedate(k)
        except:
            continue
    return dct
    
# Problem 2
    def water_data():
        

        data = requests.get('https://data.lacity.org/resource/v87k-wgde.json')
        data = json.loads(newz.content)

        water = []
        long = []
        lat = []

        for x in data:
            long.append(x['location_1']['coordinates'][0])
            lat.append(x['location_1']['coordinates'][1])
            water.append(int(x['fy_12_13']))
    
        plt.rcParams['figure.figsize'] = [10,7]
        plt.scatter(long, lat, c = water, s = water, alpha=.9)
        cbar = plt.colorbar()
        cbar.set_label('Water Use (Hundreds of cubic feet)')
        plt.show()

# Problem 3
    def books_xml():
        