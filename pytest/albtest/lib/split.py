#!/bin/python3

from urllib import parse
import re

def querysplit(query):
    querymap = {}
    querykey = query.split('=')[0]
    queryvalue = query.split('=')[1]
    querymap['Key'] = querykey
    querymap['Value'] = queryvalue

    return (querymap)


def queryConfiglist(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    
    allquerymap = []
    
    for line in lines:
            url = parse.urlparse(line)
            querylist = url.query.strip().split('&')
    
            if len(querylist) > 1:
                for query in querylist:
                    querymap = querysplit(query)
    
            else:
                querymap = querysplit(querylist[0])
    
            allquerymap.append(querymap)

    f.close()
    return (allquerymap)

def redirectConfig(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    allredirectmap = []

    for line in lines:
        redirectmap = {}
        url = parse.urlparse(line)
        if ':' in url.netloc:
            redirectmap['Host'] = url.netloc.split(':')[0]
            redirectmap['Port'] = str(url.netloc.split(':')[1])
        else:
            redirectmap['Host'] = url.netloc
            if url.scheme == 'http':
                redirectmap['Port'] = '80'
            elif url.scheme == 'https':
                redirectmap['Port'] = '443'


        redirectmap['Protocol'] = url.scheme.upper()
        redirectmap['Path'] = url.path.rstrip('\n')
        redirectmap['Query'] = url.query.rstrip('\n')
        redirectmap['StatusCode'] = 'HTTP_301'

        allredirectmap.append(redirectmap)
    
    return (allredirectmap)
