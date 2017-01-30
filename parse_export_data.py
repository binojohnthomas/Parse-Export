#!/usr/bin/python

import httplib
import json
import csv
import os
import sys
import time
import urllib
import datetime

#if(len(sys.argv) < 5):
#    print("Enter valid number of arguments: format :python <script_name> APPNAME APPLICATION_ID REST_API_KEY MASTER_KEY")
#    exit()

#APPLICATION_ID = "eMhyITg5QjAI4MWTzhinP9F6oftc7yfcr5xvLRf9"

APP_NAME = sys.argv[1]
APPLICATION_ID = sys.argv[2]
#REST_API_KEY = "1Hp1vNCpokOUqZxHKA656jOdZ3WbifO8tu5GEDH8" #REST API Key
REST_API_KEY = sys.argv[3]
MASTER_KEY =  sys.argv[4]
#MASTER_KEY = "glZL9bZXqYAGOBZfXTMETsqAswOcOEA6MKXypkQ8" #Master Key


CLASSES = "Installation" #Enter comma seperated classnames here, ex "User,Role" etc! Don't add space after/before comma.
skip = 0 # Skip these many rows, used in skip = skip_count*limit
limit = 1000 #limit number of rows per call - Max is 1000
json_file_path = "<give file path>"


def getData(app_id, rest_api_key, api_endpoint, master_key=None, limit=1000, order=None, skip=None, filter_json=None, api_version=1):
    con = httplib.HTTPSConnection('api.parse.com', 443)
    con.connect()

    header_dict = {'X-Parse-Application-Id': app_id,
                   'X-Parse-REST-API-Key': rest_api_key
                   }

   # header_dict = {'X-Parse-Application-Id': app_id,
    #               'X-Parse-REST-API-Key': rest_api_key
     #              }

    #if master_key is not None:
    #    header_dict['X-Parse-Master-Key'] = master_key

    if master_key is not None:
        header_dict['X-Parse-Master-Key'] = master_key

    params_dict = {}
    if order is not None:
        params_dict['order'] = order
    if limit is not None:
        params_dict['limit'] = limit
    if skip is not None:
        params_dict['skip'] = skip
    if filter_json is not None:
        params_dict['where'] = filter_json

    params = urllib.urlencode(params_dict)
    con.request('GET', '/%s/%s?%s' % (api_version, api_endpoint, params), '', header_dict)

    try:
        response = json.loads(con.getresponse().read())
    except Exception, e:
        response = None
        raise e

    return response

def main():
    print "*** Requesting...  ***\n"

    class_list = CLASSES.split(",") #For multiple classes!
    DEFAULT_CLASSES = {'User': 'users', 'Role': 'roles', 'File': 'files', 'Events': 'events', 'Installation': 'installations'}




    for classname in class_list:
        results = {'results': []}
        object_count = 0
        skip_count = 0
        parse_request_count = 0
        startdate = '2000-01-01T00:00:00.000Z'
        get_parse_data_startime = time.time()
        if classname not in DEFAULT_CLASSES.keys():
            endpoint = '%s/%s' % ('classes', classname)

        else:
            endpoint = DEFAULT_CLASSES[classname]


        #app_file_name = APP_NAME + str(skip_count)
        sys.stdout.write(' Fetching %s table data - ' % APP_NAME) # note if we using muliple class change APP_NAME variable to class name variable
        sys.stdout.flush()

        while True:
            startTimer = time.clock()
            skip = skip_count*limit
            filter_json = json.dumps({'createdAt': {'$gte': {'__type': 'Date', 'iso': startdate}}})


            response = getData(APPLICATION_ID, REST_API_KEY, endpoint, master_key=MASTER_KEY, order='createdAt',
                               limit=limit, skip=skip,filter_json=filter_json)
            parse_request_count += 1
            intermediate_get_parse_data_time = time.time() - get_parse_data_startime

            sys.stdout.write('  retrieved %d objects with %d reqs for %s in %.4f seconds \r' % (
            object_count, parse_request_count, classname, intermediate_get_parse_data_time))
            sys.stdout.flush()

            if 'results' in response.keys() and len(response['results']) > 1:
                # print '%s: %d, %s' % (classname, len(parse_response['results']), parse_response['results'][-1]['createdAt'])
                startdate = response['results'][-1]['createdAt']
                object_count += len(response['results'])
                results['results'].extend(response['results'])
            else:
                break





        with open(os.path.join(json_file_path, '%s.json' %APP_NAME), 'w') as json_file: # note if we using muliple class change APP_NAME variable to class name variable
            json_file.write(json.dumps(results, indent=4, separators=(',', ': ')))

        print 'Generating json... '
        parse_roundtrip_seconds = time.time() - get_parse_data_startime
        sys.stdout.write('  retrieved %d objects with %d reqs for %s in %.4f seconds \n' % (
        object_count, parse_request_count, classname, parse_roundtrip_seconds))
        sys.stdout.flush()



if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        raise e
