#!/bin/python3

import json, os
from datetime import datetime
import time

command = os.popen("aws ec2 describe-instances --query Reservations[*]")

ec2infos = json.load(command)

for ec2info in ec2infos:
    ec2ins = ec2info['Instances']
    for ec2in in ec2ins:
        for ec2tag in ec2in['Tags']:
            if ec2tag['Key'].lower() == "DeleteOn".lower():
                ec2deltime = time.mktime(datetime.strptime(ec2tag['Value'], '%Y-%m-%d').timetuple())
                today = time.mktime(datetime.today().timetuple())

                if ec2deltime - today < 0:
                    instanceids = ec2in['InstanceId']
                    if ec2in['State']['Name'] == 'running':
                        print (ec2in)

#    if (ec2info['ResourceType']) == 'instance' and (i['Key']).lower() == ('deleteon').lower():
#        bb = time.mktime(datetime.strptime(i['Value'], '%Y-%m-%d').timetuple())
#        today = time.mktime(datetime.today().timetuple())
#
#        if bb-today < 0:
#            instanceid = (i['ResourceId'])
#
#            for j in b:
#                if j['InstanceId'] == instanceid and j['InstanceState']['Name'] == 'running':
#                    os.system('aws ec2 stop-instances --instance-ids %s' %instanceid)
#                    print (instanceid + " Stop")
