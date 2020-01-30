#!/bin/python3

import sys, json
import boto3
from botocore.exceptions import ClientError
from spliturl import split

client = boto3.client('elbv2')

#response1 = client.describe_rules(
#    RuleArns=[
#        'arn:aws:elasticloadbalancing:ap-northeast-2:584946075280:listener-rule/app/test/6128197d9dabd7c7/8fe4383c24dc1d92/72796f3a29d2664d',
#    ],
#)

#print (response1)

for i in range(len(split.queryConfiglist("test.txt"))):
    conditionconfig = split.queryConfiglist("test.txt")[i]
#    actionconfig = split.redirectConfig("target.txt")[i]


    response = client.create_rule(
            ListenerArn = 'arn:aws:elasticloadbalancing:ap-northeast-2:584946075280:listener/app/test/6128197d9dabd7c7/8fe4383c24dc1d92',
            Conditions = [{'Field' : 'query-string', 'QueryStringConfig': {'Values' : [conditionconfig]}}],
            Priority= 1+i,
            Actions = [{'Type' : 'redirect', 'Order' : 1, 'RedirectConfig': {'Host': 'bori.hanbiro.net', 'Port': '80', 'Protocol': 'HTTP', 'Path': '/test/a/', 'Query': '123=234', 'StatusCode': 'HTTP_301'}}], 
    )

    print (response1)

#print (len(split.queryConfiglist("test.txt")))
