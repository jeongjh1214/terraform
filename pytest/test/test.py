#!/bin/python3

import sys
import boto3


client = boto3.client('rds')
a = client.list_tags_for_resource(ResourceName='arn:aws:rds:ap-northeast-2:779475221336:db:mysql-an2-ss-newrelic')['TagList']

print (a)
