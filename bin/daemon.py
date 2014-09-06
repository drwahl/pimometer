#!/usr/bin/env python

import time
import pimometer
try:
    from pymongo import Connection
    pymongo_driver = True
except ImportError:
    import urllib2
    pymongo_driver = False
import json

def connect(collection):
    """
    Return a mongodb cursor
    """
    if pymongo_driver:
        cursor = collection.find()
    else:
        cursor = json.load(urllib2.urlopen(collection))['rows']

    return cursor

def get_poll_interval(collection):
    """
    Determine the configured poll interval or make one up
    """
    cursor = connect(collection)
    try:
        poll_interval = cursor['client_config']['poll_interval']
    except:
        poll_interval = 60
        collection.update(
                {'_id': 'client_config'},
                {"$set": {
                    'poll_interval': poll_interval}},
                upsert=True)

    return poll_interval

def get_current_event(collection):
    """
    Determine the configured event
    """
    cursor = connect(collection)
    try:
        event = cursor['client_config']['current_event']
    except:
        event = None
        collection.update(
                {'_id': 'client_config'},
                {"$set": {
                    'current_event': event}},
                upsert=True)

    return event

def run():
    coll = pimometer.configure()
    current_event = None
    while True:
        poll_interval = get_poll_interval(coll)
        event = get_current_event(coll)

        if event != None:
            client_collection = pimometer.configure()
            sensor1 = None #this needs to pull data from the sensor
            sensor2 = None #this needs to pull data from the sensor
            pimometer.update_event(event=event, s1=sensor1, s2=sensor2, collection=client_collection)

        time.sleep(poll_interval)

if __name__ == "__main__":
    run()
