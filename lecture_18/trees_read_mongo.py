"""
@author John Rachlin
@date   Nov 16, 2021
@file   trees_read_mongo.py
@class  DS3500: Intermediate programming with data
"""


import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import math


def gps_to_xy(coords, boundary, size=(1000, 1000)):
    """ Map gps (lon,lat) coordinates to
    array coordinates based on the bounderies given as
    (minlon, minlat, maxlon, maxlat) and the size
    (height, width) of the array. Return array coordinates. """
    lon, lat = coords
    minlon, minlat, maxlon, maxlat = boundary
    height, width = size
    i = height - (lat - minlat) / (maxlat - minlat) * height
    j = (lon - minlon) / (maxlon - minlon) * width
    return int(i), int(j)

def plot_trees(trees, boundary, shape=(1000,1000)):

    minlon, minlat, maxlon, maxlat = boundary
    arr = np.zeros(shape=shape)


    for tree in trees:
        gps = tree['geometry']['coordinates']
        x, y = gps_to_xy(gps, boundary, shape)
        if 0 <= x < shape[0] and 0 <= y < shape[1]:
            if tree['properties']['TYPE'] == 'PARK-TREE':
                arr[x,y] = 1
            else:
                arr[x,y] = 2

    plt.figure(figsize=(10, 10))
    plt.grid()

    latticks = np.arange(0, shape[0], shape[0] / 6)
    latlabels = [round(x,3) for x in np.arange(maxlat, minlat, (minlat-maxlat)/6)]
    plt.yticks(ticks=latticks, labels=latlabels)

    lonticks=np.arange(0, shape[1], shape[1]/6)
    lonlabels=[round(x,3) for x in np.arange(minlon, maxlon, (maxlon-minlon)/6)]
    plt.xticks(ticks=lonticks, labels=lonlabels)

    plt.xlabel('GPS Longitude')
    plt.ylabel('GPS Latitude')

    #plt.imshow(arr, cmap='viridis')
    plt.imshow(arr, cmap='viridis', interpolation='none')
    plt.show()

def main():

    # Load Park Tree Data
    client = MongoClient()
    db = client.boston
    trees = db.trees.find({})

    # Some boundary conditions
    shape = (400, 400) # Change to (300,300) for NEU
    boston = (-71.2, 42.2, -70.9, 42.4)
    northeastern = (-71.099385, 42.333418, -71.076298, 42.343818)
    plot_trees(trees, boston, shape)



if __name__ == '__main__':
    main()
