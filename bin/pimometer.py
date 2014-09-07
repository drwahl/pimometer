#!/usr/bin/env python
# vim: set expandtab:
"""
**********************************************************************
GPL License
***********************************************************************
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

***********************************************************************/

:author: David Wahlstrom
:email: david.wahlstrom@gmail.com

"""

import datetime
import sys
import logging
import os
try:
    from pymongo import Connection
    pymongo_driver = True
except ImportError:
    import urllib2
    pymongo_driver = False
import json
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
if os.path.isfile('/etc/pimometer/pimometer.conf'):
    config = '/etc/pimometer/pimometer.conf'
else:
    config = os.path.join(os.path.dirname(__file__), '../conf/pimometer.conf')
parser.read(config)

mongodb_host = parser.get('pimometer', 'host')
dbname = parser.get('pimometer', 'database')
collection_name = parser.get('pimometer', 'collection')

logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%y.%m.%d %H:%M:%S')
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger('pimometer').addHandler(console)
log = logging.getLogger('pimometer')


def configure():
    """
    Read configuration file and intialize connection to the mongodb instance
    """
    log.debug('in configure')

    host = mongodb_host
    log.debug('connecting to mongodb host: %s' % host)
    database = dbname
    log.debug('connecting to database name: %s' % database)
    collection = collection_name
    log.debug('using collection name: %s' % collection)
    if pymongo_driver:
        log.debug('using pymongo driver for communications')
        con = Connection(host)
        log.debug('selecting database/collection: %s/%s' % (database,
                                                            collection))
        col = con[database][collection]
    else:
        log.debug('using REST interface for communications')
        col = 'http://%s/%s/%s/' % (host, database, collection)
    return col


def update_event(collection, event, s1, s2, timestamp):
    """
    Update <event> document in MongoDB with tempuratures of sensor 1 (<s1>) and
    sensor 2 (<s2>).
    """
    log.debug("in update_event(%s, %s, %s, %s, %s)" % (collection, event,
                                                       s1, s2, timestamp))

    s1_existing_data = collection.find_one({'_id': event})['s1']
    s2_existing_data = collection.find_one({'_id': event})['s2']

    if s1_existing_data:
        s1_data = s1_existing_data + [{timestamp: s1}]

    if s2_existing_data:
        s2_data = s2_existing_data + [{timestamp: s2}]

    collection.update(
        {'_id': event},
        {"$set": {
            's1': s1_data,
            's2': s2_data}},
        upsert=True)


def get_event_data(collection, event):
    """
    Dump event data for <event>.
    """
    log.debug("in get_event_data(%s, %s)" % (collection, event))

    result = collection.find_one({'_id': event})

    return result


def main():
    import argparse

    cmd_parser = argparse.ArgumentParser(description='CLI for pimometer data.')
    cmd_parser.add_argument(
        '-g',
        '--get',
        dest='get_event',
        action='store',
        help='Get the data from the specified event',
        default=None)
    cmd_parser.add_argument(
        '-1',
        '--sensor1',
        dest='s1',
        action='store',
        help='Tempurature data from sensor 1',
        default=None)
    cmd_parser.add_argument(
        '-2',
        '--sensor2',
        dest='s2',
        action='store',
        help='Tempurature data from sensor 2',
        default=None)
    cmd_parser.add_argument(
        '-e',
        '--event',
        dest='event',
        action='store',
        help='Event of bbq/smoke out',
        default=None)
    cmd_parser.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='Enable debugging during execution',
        default=None)
    args = cmd_parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    collection = configure()

    if args.get_event:
        print get_event_data(collection, args.get_event)
    else:
        if not args.event or not args.s1 or not args.s2:
            print "ERROR: -1, -2, or -e not specified.\n"
            cmd_parser.print_help()
            sys.exit(1)
        else:
            now = datetime.datetime.now().isoformat()
            update_event(collection, args.event, args.s1, args.s2, now)

if __name__ == "__main__":
    main()
