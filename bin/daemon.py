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


def get_poll_interval(collection):
    """
    Determine the configured poll interval or make one up
    """
    poll_interval = 60  # set a default poll_interval
    try:
        poll_interval = collection.find_one(
            {'_id': 'client_config'})['poll_interval']
    except TypeError:
        collection.update(
            {'_id': 'client_config'},
            {"$set": {
                'poll_interval': poll_interval}},
            upsert=True)
        poll_interval = collection.find_one(
            {'_id': 'client_config'})['poll_interval']

    assert type(poll_interval) == int

    return poll_interval


def get_current_event(collection):
    """
    Determine the configured event
    """
    event = None  # set a default event
    try:
        event = collection.find_one(
            {'_id': 'client_config'})['current_event']
    except:
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

        # generate "random" data in for the event "demo"
        # this is mostly useful for development/testing
        if demo:
            poll_interval = 5
            # random data for demo/test purposes
            sensor1 = float(random.randrange(170, 190))
            sensor2 = float(sensor1 - random.randrange(1, 4))
            pimometer.update_event(event='demo',
                                   s1=sensor1,
                                   s2=sensor2,
                                   collection=client_collection,
                                   timestamp=timestamp)

        if event is not None:
            sensor1 = 1.0  # need to pull data from sensor1
            sensor2 = 2.0  # need to pull data from sensor2
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
