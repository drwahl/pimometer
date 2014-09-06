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
    """Read configuration file and intialize connection to the mongodb instance"""
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
        log.debug('selecting database/collection: %s/%s' % (database, collection))
        col = con[database][collection]
    else:
        log.debug('using REST interface for communications')
        col = 'http://%s/%s/%s/' % (host, database, collection)
    return col


def update_config(collection, event=None, poll_interval=60):
    """
    Update client configuration collection
    """
    log.debug("in update_config(%s, %s, %s,)" % (collection, event, poll_interval))

    if pymongo_driver:
        cursor = collection.find()
    else:
        cursor = json.load(urllib2.urlopen(collection))['rows']

    if event == 'None':
        event = None

    collection.update(
            {'_id': 'client_config'},
            {"$set": {
                'current_event': event,
                'poll_interval': float(poll_interval)}},
            upsert=True)

def get_config(collection):
    if pymongo_driver:
        cursor = collection.find()
    else:
        cursor = json.load(urllib2.urlopen(collection))['rows']

    result = None

    for doc in cursor:
        if doc['_id'] == 'client_config':
            result = doc

    return result


def main():
    import argparse

    cmd_parser = argparse.ArgumentParser(description='Configure client_config for pimometer')
    cmd_parser.add_argument(
        '-g',
        '--get',
        dest='get_config',
        action='store_true',
        help='Returns the current configuration for client_config',
        default=None)
    cmd_parser.add_argument(
        '-p',
        '--poll-interval',
        dest='poll_interval',
        action='store',
        help='Value to set the poll interval to.',
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

    if args.get_config:
        print get_config(collection)
    else:
        if not args.event and not args.poll_interval:
            print "ERROR: -e or -p not specified.\n"
            cmd_parser.print_help()
            sys.exit(1)
        else:
            if args.event and args.poll_interval:
                update_config(collection, args.event, args.poll_interval)
            elif args.event:
                update_config(collection, event=args.event)
            elif args.poll_interval:
                update_config(collection, poll_interval=args.poll_interval)


if __name__ == "__main__":
    main()
