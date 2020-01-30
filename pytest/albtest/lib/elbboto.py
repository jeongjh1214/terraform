#!/bin/python3

import sys, json
import boto3
from botocore.exceptions import ClientError
from . import split

def lenrule(arn):
    client = boto3.client('elbv2')

    response = client.describe_rules(
            ListenerArn = arn,
            )

    return (len(response['Rules']))

def makealbrule(arn,sourcefile,targetfile):
    client = boto3.client('elbv2')

    if lenrule(arn) + len(split.queryConfiglist(sourcefile)) > 99:
        print ("기존 정책 및 추가될 정책 생성 시 제한 초과합니다. (최대 100개 기준)")
        print ("기존정책 %d, 추가될 정책 %d 입니다" %(lenrule(arn),len(split.queryConfiglist(sourcefile))))
        sys.exit()

    if len(split.queryConfiglist(sourcefile)) > 99:
        print ("정책 추가 제한을 넘었습니다. (최대 100개 기준)")
        sys.exit()

    
    for i in range(len(split.queryConfiglist(sourcefile))):
        conditionconfig = split.queryConfiglist(sourcefile)[i]
        actionconfig = split.redirectConfig(targetfile)[i]
    
        response = client.create_rule(
                ListenerArn = arn, 
                Conditions = [{'Field' : 'query-string', 'QueryStringConfig': {'Values' : [conditionconfig]}}],
                Priority= 1+i,
                Actions = [{'Type' : 'redirect', 'Order' : 1, 'RedirectConfig': actionconfig}], 
        )
    
        return (response)
    
