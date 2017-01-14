import json
import datetime
import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et

from pyproj import Proj, transform
from scipy.spatial import cKDTree

# Problem 1
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        pass

def DateTimeDecoder(item):
    pass

# Problem 2
# Provide a solution to this problem in a separate file

# Problem 3
def prob3():
    print "The author with the most expensive book is", None
    print "The number of books published before Dec 1, 2000 is", None
    print "The books that reference Microsoft in their description are", None


# Problem 4
def convert(longitudes, latitudes):
    from_proj = Proj(init="epsg:4326")
    to_proj = Proj(init="epsg:3857")

    x_vals = []
    y_vals = []
    for lon, lat in zip(longitudes, latitudes):
        x, y = transform(from_proj, to_proj, lon, lat)
        x_vals.append(x)
        y_vals.append(y)

    return x_vals, y_vals

def prob4():
    pass

if __name__ == "__main__":
    pass
