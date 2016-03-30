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

import xively
from datetime import datetime
import json
import geojson
from collections import OrderedDict
from flask import Flask, request, Response

wsgi_app = Flask(__name__, static_url_path='')
wsgi_app.debug = True

@wsgi_app.route('/')
def root():
    return wsgi_app.send_static_file('index.html')

def get_feeds(query):
    """Returns a GeoJSON document with a list of feeds."""
    data = xively.list_feeds(query=query)
    features = [];
    for datum in data:
        name = datum['name']
        status = datum['status']
        json_url = "/feeds/" + str(datum['id']) + ".json";
        url = "/view.html?json=" + json_url + "&h1=.properties%20.name&h2=Datastreams&table=.features%20.properties%20.datastreams";
        feature = geojson.Feature(geometry=geojson.Point((datum['longitude'], datum['latitude'])),
                                  id = datum['id'],
                                  properties= OrderedDict([("name", name), ("status", status), ("url", url)]))
        features.append(feature)
    features = sorted(features, key=lambda feature: feature['properties']['name'])
    return geojson.dumps(geojson.FeatureCollection(features))


@wsgi_app.route('/live.json')
def get_live_feeds():
    return get_feeds('?user=iostp&content=summary&status=live&per_page=1000');

@wsgi_app.route('/frozen.json')
def get_frozen_feeds():
    return get_feeds('?user=iostp&content=summary&status=frozen&per_page=1000');

@wsgi_app.route('/all.json')
def get_all_feeds():
    return get_feeds('?user=iostp&content=summary&per_page=1000');

@wsgi_app.route('/peterborough.json')
def get_peterborough_feeds():
    return get_feeds('?user=iostp&content=summary&lat=52.5695&lon=-0.2405&distance=12&per_page=1000');

@wsgi_app.route('/singapore.json')
def get_singapore_feeds():
    return get_feeds('?user=iostp&content=summary&lat=1.2902&lon=103.851&distance=300&per_page=1000');

@wsgi_app.route('/feeds/<feed_id>.json', methods=['GET'])
def get_feed(feed_id):
    data = xively.get_feed(feed_id).json()

    name = data['location']['name']

    datastreams = xively.datastreams(data)

    for datastream in datastreams:
        id = datastream['id']
        url = "/view.html?json=/feeds/" + str(feed_id) + "/datastreams/" + str(id) + ".json" + "&h1=" + name + "&h2=.label"
        datastream.update({'url': url})
        
    feature = geojson.Feature(geometry=geojson.Point((data['location']['lon'], data['location']['lat'])),
                              id = data['id'],
                              properties= {"name": name, 'datastreams' : datastreams})
        
    return geojson.dumps(geojson.FeatureCollection([feature]))

    
@wsgi_app.route('/feeds/<feed_id>/datastreams/<datastream_id>.json', methods=['GET'])
def get_datastream(feed_id, datastream_id):

    data = xively.get_datastream(feed_id, datastream_id, range = xively.make_range(start=xively.month_start(datetime.now()), duration='1day', interval=3600, limit=1000)).json()

    json_root = "/feeds/" + str(feed_id) + "/datastreams/"  + str(datastream_id) + "/datapoints/";
    day_url = json_root + "day.json"
    month_url = json_root + "month.json"
    year_url = json_root + "year.json"
    all_url = json_root + "all.json"

    label = data['unit']['label']
    h1 =  label

    day_url = "/view.html?json=" + day_url + "&h1=" + label + "&h2=Last day";
    month_url = "/view.html?json=" + month_url + "&h1=" + label + "&h2=Last month";
    year_url = "/view.html?json=" + year_url + "&h1=" + label + "&h2=Last year";
    all_url = "/view.html?json=" + all_url + "&h1=" + label + "&h2=All";
    
    data2= OrderedDict([("at", data['at']),
                        ("label", label),
                        ("symbol", data['unit']['symbol']),
                        ("current_value", data['current_value']),
                        ("max_value", data['max_value']),
                        ("min_value", data['min_value']),
                        ("last_day", day_url),
                        ("last_month", month_url),
                        ("last_year", year_url),
                        ("all", all_url)])


    
    return json.dumps(data2)

# Last day

@wsgi_app.route('/feeds/<feed_id>/datastreams/<datastream_id>/datapoints/day.json', methods=['GET'])
def get_datapoints_day(feed_id, datastream_id):
    data = xively.list_datapoints(feed_id, datastream_id, range = xively.make_range(duration='1day', interval=3600, limit=1000))
    return json.dumps(data)

# Last month

@wsgi_app.route('/feeds/<feed_id>/datastreams/<datastream_id>/datapoints/month.json', methods=['GET'])
def get_datapoints_month(feed_id, datastream_id):
    return json.dumps(xively.list_datapoints(feed_id, datastream_id, range = xively.make_range(duration='1month', interval=86400, limit=1000)))

# Last year

@wsgi_app.route('/feeds/<feed_id>/datastreams/<datastream_id>/datapoints/year.json', methods=['GET'])
def get_datapoints_year(feed_id, datastream_id):
    return json.dumps(xively.list_datapoints(feed_id, datastream_id, range = xively.make_range(duration='1year', interval=86400, limit=1000)))

# All data (since 2014)

@wsgi_app.route('/feeds/<feed_id>/datastreams/<datastream_id>/datapoints/all.json', methods=['GET'])
def get_datapoints_all(feed_id, datastream_id):
    return json.dumps(xively.daily_datapoints(feed_id, datastream_id, from_date= datetime(2014,1,1,0,0,0,0)))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 5555, wsgi_app)
    httpd.serve_forever()
