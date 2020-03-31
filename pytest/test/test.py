#!/bin/python3

import sys
import boto3
import time, datetime

a = '24-03-2020'
a = time.strptime(a, '%d-%m-%Y')
b = datetime.datetime.now().strftime('%d-%m-%Y')
b = time.strptime(b, '%d-%m-%Y')


if a <= b:
    print ("abc")
