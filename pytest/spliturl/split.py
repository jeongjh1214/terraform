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
                addquerymap = []
                for query in querylist:
                    querymap = querysplit(query)
                    addquerymap.append(querymap)
    
            else:
                querymap = querysplit(querylist[0])
                addquerymap = [querymap]
    
            allquerymap.append(addquerymap)

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
            redirectmap['Port'] = url.netloc.split(':')[1]
        else:
            redirectmap['Host'] = url.netloc
            if url.scheme == 'http':
                redirectmap['Port'] = '80'
            elif url.scheme == 'https':
                redirectmap['Port'] = '443'


        redirectmap['Protocol'] = url.scheme
        redirectmap['Path'] = url.path
        redirectmap['Query'] = url.query.rstrip('\n')
        redirectmap['StatusCode'] = 'HTTP_301'

        allredirectmap.append(redirectmap)
    
    return (allredirectmap)

print (redirectConfig("test.txt")[0])
