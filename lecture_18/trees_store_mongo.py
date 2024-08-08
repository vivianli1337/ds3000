"""
trees_store_mongo.py
Demonstration of storing data in mongo
Requires pymongo library: conda install pymongo
Also requires that you have a mongo server running
"""

from pymongo import MongoClient
import json


def main():

    # Load Tree Data and verify
    with open('trees.geojson', 'r') as trees_file:
        trees = json.load(trees_file)

    print("Number of trees: ", len(trees['features']))
    print("One of the trees: ", trees['features'][0])


    # Transformation - OPTIONAL SIMPLIFICATION OF SCHEMA
    #transformed = [{'type': tree['properties']['TYPE'],
    #                'coord':tree['geometry']['coordinates']}
    #               for tree in trees['features']]

    # connect to mongo
    client = MongoClient()

    # Clear old instances
    client.drop_database('boston')

    # Create new database instance
    db = client.boston

    # Store each tree in the tree collection of the boston database
    print('Loading trees into mongo')
    db.trees.insert_many(trees['features'])
    print('Finished loading')


if __name__ == '__main__':
    main()

