#!/bin/python3

import sys, json
import boto3
from botocore.exceptions import ClientError
from lib import elbboto 
from lib import split


#print (split.filecmp("target.txt","test.txt"))
print (split.filenum("target.txt"))
