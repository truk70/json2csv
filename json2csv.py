#!/bin/python3
# This script converts a list of nested json items to flat csv table. 
# Niiice!
# for more information, how to use it, execute the following:
# python3 json2csv.py -h   
# Author: kurtgerber70@gmail.com
# Date: 29.03.2021
# 

import json 
import csv 
import sys

def __crop_to_list(json_data, jsonpath):
    # converting path string into a list
    path_list = jsonpath.split(".")

    # for each element in path_list, slice the data a bit more
    for k in path_list:
        try:
            json_data = json_data[k]
        except:
            print("Path element %s not found", k)
            sys.exit(1)
    return(json_data)


def __list_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in __list_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in __list_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]

def __dict_generator(inlist):
    dict_out = {}
    for item in inlist:
        myval = item.pop()
        myval = myval
        if len(item)>1:
            mykey = ".".join(item)
        else:
            mykey=item[0]
        dict_out[mykey]=str(myval).strip()
        
    return(dict_out)


def json2csv(data,jsonpath,csv_file):
    # data: dictionary loaded with json.load()
    # csv_file: file path and name to which the csv output will be written

    # now we will open a file for writing 
    data_file = open(csv_file, 'w',newline='') 
  
    # create the csv writer object 
    csv_writer = csv.writer(data_file) 

    # Counter variable used for writing  
    # headers to the CSV file 

    data = __crop_to_list(data,jsonpath)
    count = 0
    header = None
    for item in data: 
        data_dict_flat = __dict_generator(__list_generator(item))
        if count == 0:
            #Writing headers of CSV file 
            header = data_dict_flat.keys() 
            csv_writer.writerow(header) 
        else:  
            # Writing data of CSV file
            row = []
            for header_key in header:
                row+= [data_dict_flat.get(header_key,"")]
                
            csv_writer.writerow(row) 
        count =+ 1 
  
    data_file.close()


if __name__ == "__main__":
    import os.path
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('jsonpath', help="defines json path to the list to parse. Example: data.deals")
    parser.add_argument('file', help="path to json file to parse")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print("Needs a valid json file as argument")
        parser.print_help()
        sys.exit(1)

    # Opening JSON file and loading the data 
    # into the variable data 
    with open(args.file) as json_file: 
        data = json.load(json_file)

    

    #Create the output file name based on the input file name
    mypath,myfile = os.path.split(args.file)
    base_file,ext = os.path.splitext(myfile)
    out_file = '.'.join((base_file,'csv')) 
    csv_file = os.path.join(mypath,out_file) 

    # Execute the the transformation
    json2csv(data,args.jsonpath,csv_file)

  
 