#!/bin/python3

from urllib import parse
import re


f = open("i.txt", 'r')
lines = f.readlines()
for line in lines:
        url = parse.urlparse(line)
        a = re.findall('testReq=[0-9]{5}',url.query.strip())

        if len(a) > 0:
                print (a[0] + '\t' + str(len(a)))
        else:
                print (" ")
