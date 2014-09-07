#!/usr/bin/env python

import datetime
import sys
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
    try:
        poll_interval = collection.find_one({'_id': 'client_config'})['poll_interval']
    except TypeError:
        poll_interval = 60
        collection.update(
                {'_id': 'client_config'},
                {"$set": {
                    'poll_interval': float(poll_interval)}},
                upsert=True)

    return poll_interval

def get_current_event(collection):
    """
    Determine the configured event
    """
    try:
        event = collection.find_one({'_id': 'client_config'})['current_event']
    except:
        event = None
        collection.update(
                {'_id': 'client_config'},
                {"$set": {
                    'current_event': event}},
                upsert=True)

    return event

def run(demo=False):
    coll = pimometer.configure()
    current_event = None
    while True:
        poll_interval = get_poll_interval(coll)
        event = get_current_event(coll)
        client_collection = pimometer.configure()
        timestamp = datetime.datetime.now().isoformat()

        #generate "random" data in for the event "demo"
        #this is mostly useful for development/testing
        if demo:
            poll_interval = 5
            sensor1 = float(random.randrange(170, 190)) #random data for demo/test purposes
            sensor2 = float(sensor1 - random.randrange(1, 4)) #random data for demo/test purposes
            pimometer.update_event(event='demo',
                                   s1=sensor1,
                                   s2=sensor2,
                                   collection=client_collection,
                                   timestamp=timestamp)

        if event != None:
            sensor1 = 1 #need to pull data from sensor1
            sensor2 = 2 #need to pull data from sensor2
            pimometer.update_event(event=event,
                                   s1=sensor1,
                                   s2=sensor2,
                                   collection=client_collection,
                                   timestamp=timestamp)

        time.sleep(poll_interval)

if __name__ == "__main__":
    demo_run = False
    try:
        if sys.argv[1] == "demo=True":
            demo_run = True
        else:
            demo_run = False
    except IndexError:
        demo_run = False

    if demo_run:
        import random
        run(demo=True)
    else:
        run(demo=False)
