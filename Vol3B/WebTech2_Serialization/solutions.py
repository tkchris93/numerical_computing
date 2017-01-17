import json
import datetime
import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et

from pyproj import Proj, transform
from scipy.spatial import cKDTree

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'dtype': 'datetime',
                    'year': obj.year,
                    'month': obj.month,
                    'day': obj.day,
                    'hour': obj.hour,
                    'minute': obj.minute,
                    'second': obj.second,
                    'microsecond': obj.microsecond}

def DateTimeDecoder(item):
    if item["dtype"] != 'datetime':
        raise ValueError("Object passed to decoder is not a datetime object")
    else:
        y = item["year"]
        mo = item["month"]
        d = item["day"]
        h = item["hour"]
        mi = item["minute"]
        s = item["second"]
        mu_s = item["microsecond"]
        return datetime.datetime(y, mo, d, h, mi, s, mu_s)

def prob3():
    t = et.parse("books.xml")
    root = t.getroot()
    children = list(root)
   
    author = []
    title = []
    genre = []
    price = []
    publish_date = []
    description = []     
    for c in children:
        try:
            author.append(c.find("author").text)
        except:
            author.append("")
        try:
            title.append(c.find("title").text)
        except:
            title.append("")
        try:
            genre.append(c.find("genre").text)
        except:
            genre.append("")
        try:
            price.append(c.find("price").text)
        except:
            price.append("")
        try:
            publish_date.append(c.find("publish_date").text)
        except:
            publish_date.append("")
        try:
            description.append(c.find("description").text)
        except:
            description.append("")

    d = {"author":author, "title":title, "genre":genre, "price":price, "publish_date":publish_date, "description":description} 

    books = pd.DataFrame(d)        

    books.publish_date = books.publish_date.apply(lambda s : datetime.datetime.strptime(s, "%Y-%m-%d"))


    print "The author with the most expensive book is", books.author[books.price.argmax()]
    print "The number of books published before Dec 1, 2000 is", books[books.publish_date < datetime.datetime(2000, 12, 1)].shape[0]

    print "The books that reference Microsoft in their description are", books[books.description.str.find("Microsoft") != -1].title.tolist()

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
    data = requests.get("https://data.cityofnewyork.us/api/views/sxx4-xhzg/rows.xml?accessType=DOWNLOAD").content
    tree = et.fromstring(data[10:-11])
    children = list(tree)
    lat = []
    lon = []
    for i in xrange(len(children)):
        try:
            lat.append(children[i].find("latitude").text)
            lon.append(children[i].find("longitude").text)
        except Exception:
            pass

    lon, lat = convert(lon, lat)
    cans = np.hstack((np.vstack(lon), np.vstack(lat))).astype(np.float64)
  
    ny_df = pd.read_csv("random_newyork_locations.csv")

    ny_lon, ny_lat = convert(ny_df["longitude"], ny_df[ "latitude"])
    ny_locations = np.hstack((np.vstack(ny_lon), np.vstack(ny_lat))).astype(np.float64)

    kdtree = cKDTree(cans)
    dist, ind = kdtree.query(ny_locations, k=1)

    return np.average(dist) / 1000 * 0.621371    

if __name__ == "__main__":
    pass
