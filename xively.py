#!/usr/bin/env python3

# (C) Copyright 2016 Rob Blackwell
# All rights reserved.

# This software is provided "as is" without warranty of any kind,
# express or implied, including but not limited to warranties as to
# quality and fitness for a particular purpose.

# Rob Blackwell does not support the Software, nor does he warrant
# that the Software will meet your requirements or that the operation
# of the Software will be uninterrupted or error free or that any
# defects will be corrected.

from datetime import datetime, timedelta
import requests
import calendar
from collections import OrderedDict

KEY = '8cyHFd7vHCYeJ4x0mOEcgFmkOPUheWtK4Nu1YTOyKhxwFsLC'

# Calendar date utilities

def month_start(dt):
    """Returns the datetime at the start of the month in which the given datetime lies."""
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def month_end(dt):
    """Returns the datetime at the end of the month in which the given datetime lies."""
    (first, end) = calendar.monthrange(dt.year, dt.month)
    return dt.replace(day= end, hour=23, minute=59, second=59, microsecond=999999)

def next_month_start(dt):
    """Returns the datetime at the start of the next month after the month in which the given datetime lies."""
    return month_start(dt + timedelta(days=32))

def monthly_ranges(from_date, to_date):
    """Returns pairs of start, end dates being the segments of the given span of time split into months or partial months."""
    start = from_date
    end = month_end(start)
    while end < to_date:
        yield (start,end)
        start = next_month_start(start)
        end = month_end(start)
    yield(start, to_date)

# Low level API
def get_feed(feed_id, range='', key = KEY):
    url = 'https://api.xively.com/v2/feeds/' + str(feed_id)  + range 
    headers = {'X-ApiKey': key}
    r = requests.get(url,  headers=headers)
    return r

def get_feeds(query='', key = KEY):
    url = 'https://api.xively.com/v2/feeds'  + query 
    headers = {'X-ApiKey': key}
    r = requests.get(url,  headers=headers)
    return r

def get_datastream(feed_id, datastream_id, range='', key = KEY):
    url = 'https://api.xively.com/v2/feeds/' + str(feed_id) + '/datastreams/' + str(datastream_id) + range 
    headers = {'X-ApiKey': key}
    r = requests.get(url,  headers=headers)
    return r

# Range queries

def make_range(start=None, end= None, duration=None, interval_type=None, interval=None, limit=None):
    buffer = '?'
    if start is not None:
        buffer += 'start=' + start.isoformat() + '&'
    if end is not None:
        buffer += 'end=' + end.isoformat() + '&'
    if duration is not None:
        buffer += 'duration=' + duration + '&'
    if interval_type is not None:
        buffer += 'interval_type=' + interval_type + '&'
    if interval is not None:
        buffer += 'interval=' + str(interval) + '&'
    if duration is not None:
        buffer += 'limit=' + str(limit) + '&'
    return buffer[:-1]

DEFAULT_RANGE = make_range(start=month_start(datetime.now()), duration='1month', interval=86400, limit=1000)

# High Level API

def list_feeds(query='?user=iostp&content=summary', key=KEY):
    """Returns a list of [feed_id, name, lon, lat, lon] for each feed in the list of feeds owned by user."""
    l = []
    for x in get_feeds(query=query, key=key).json()['results']:
        if 'location' in x and 'name' in x['location'] and 'lat' in x['location'] and 'lon' in x['location'] :
            id = x['id']
            name = x['location']['name']
            lon = x['location']['lon']
            lat = x['location']['lat']
            status = x['status']
            #l.append([id, name, lon, lat])
            l.append(OrderedDict([('id' , id), ('name' , name), ('status' , status), ('longitude' , lon), ('latitude' , lat)]))
    return l

def datastreams(data):
    """Returns a table of datastreams extracted from the given data."""
    l = []
    if 'datastreams' in data:
        for datastream in data['datastreams']:
            datastream = OrderedDict([('id' , datastream['id']),
                                      ('label' , datastream.get('unit', {}).get('label','')),
                                      ('symbol' , datastream.get('unit', {}).get('symbol','')),
                                      ('at' , datastream['at']),
                                      ('current_value' , datastream['current_value']),
                                      ('max_value' , datastream['max_value']),
                                      ('min_value' , datastream['min_value'])])
            l.append(datastream)
            
    return l
    
def list_datastreams(feed_id, key=KEY):
    """Returns a table of datastreams from the given feed."""

    feed = get_feed(feed_id, key=key).json()
    
    return datastreams(feed)



def list_datapoints(feed_id, datastream_id, range=DEFAULT_RANGE, key=KEY):
    """Returns a list of [datetime, value] for each datapoint in the given datastream."""
    l = []
    datastream = get_datastream(feed_id, datastream_id, range, key=key).json()
    if 'datapoints' in datastream:
        for datapoint in datastream['datapoints']:
             l.append(OrderedDict([('at' ,  datapoint['at']), ('value' ,datapoint['value'])]))
    return l

def daily_datapoints(feed_id, datastream_id, from_date, to_date=None, key=KEY):
    """Returns a list of daily [datetime, value] for each datapoint in the given datastream between from_date and to_date."""
    if to_date is None:
        to_date = datetime.now()
    l = []
    months = monthly_ranges(from_date, to_date)
    for start, end in months:
        x = list_datapoints(feed_id, datastream_id, make_range(start=start, end=end, interval_type='discrete', interval=86400, limit=1000), key=key)
        l += x
    return l


