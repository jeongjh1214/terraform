#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
import re, datetime


#ec2 = boto3.client('elbv2')
#response = ec2.describe_load_balancers()


#for i in response['LoadBalancers']:
#    arnname = i['LoadBalancerArn']

#test = ec2.describe_tags(ResourceArns=[a['LoadBalancerArn'] for a in response['LoadBalancers']])
#b = [i['ResourceArn'] for i in test['TagDescriptions'] if i['Tags'] == []]
#
#for bb in b:
#    aaa = ec2.describe_target_groups(LoadBalancerArn=bb)
#    c = [cc['TargetGroupArn'] for cc in aaa['TargetGroups'] if cc['TargetType'] == 'instance']
#
#    test2 = ec2.describe_target_health(TargetGroupArn=c[0])
#    print (test2['TargetHealthDescriptions'])


#ec2 = boto3.client('iam')
#response = ec2.

#ec2 = boto3.client('sts')
#response = ec2.get_caller_identity().get('Account')
#
#print (response)

ec2 = boto3.client('ec2')
response = ec2.describe_security_groups()

for i in response['SecurityGroups']:
    for j in i['IpPermissions']:
        if 'Description' in j.keys():
            print ("abc")
        else:
            print (j)
#        if j['PrefixListIds']:
#            print (j)
 

