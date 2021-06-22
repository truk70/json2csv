#!/usr/bin/python3
# Request json from a graphql api and convert it to a csv file with json2csv.py.
# Author: kurtgerber70@gmail.com
# Date: 1.4.2021

import json
import requests
import sys
from json2csv import json2csv


def do_request(url,g_def):
    req_data = {"query" : g_def}
    req_json = json.dumps(req_data)
    header = {'Accept':'application/json','Content-type':'application/json','Accept-Encoding':'gzip,deflate,br'}
    try:
        req = requests.post(url=url,headers=header,data=req_json)
    except:
        print("Web request failed.")
        print("Status code:")
        print(req.status_code)
        sys.exit(1)
    print(req.status_code)
    try:
        json_data = json.loads(req.text)
    except:
        print("Response is not valid json:\n")
        print(req.text)
    return json_data


if __name__ == "__main__":
    import os.path
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-g','--graphql' , type=str, default="request.graphql", help="File containing graphql request body")
    parser.add_argument('-j','--jsonpath', type=str, default="data.deals", help="defines json path to the list to parse. Example: data.deals")
    parser.add_argument('url', help="URL of the graphql api to request data from")


    args = parser.parse_args()

    if not os.path.isfile(args.graphql):
        print("Needs a valid request definition file. Default name: request.graphql")
        parser.print_help()
        sys.exit(1)
    
    with open(args.graphql,'r') as g_file:
        g_req = g_file.read()

    if not args.url:
        print("Need a valid URL to start a request. None given.")
        parser.print_help()
        sys.exit(1)

    json2csv(do_request(args.url,g_req),args.jsonpath,"output.csv")