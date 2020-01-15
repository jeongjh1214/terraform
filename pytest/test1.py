#!/bin/python3

import json, os, sys
from datetime import datetime
import time


command = os.popen("aws ec2 describe-instances --query Reservations[*]")
command2 = os.popen("aws ec2 describe-tags --query Tags[*]")

ec2infos = json.load(command)
ec2tagsinfos = json.load(command2)

#deleteon 있는 서버
deloninstanceids = []

# deleteon 없는 서버
deloninstanceids2 = []

for ec2info in ec2infos:
    ec2ins = ec2info['Instances']
    for ec2in in ec2ins:
        if 'Tags' not in ec2in.keys():
            print ("no tags " + ec2in['InstanceId'])
        else:
            delcount = 0
            for ec2tag in ec2in['Tags']:
                if "DeleteOn".lower() in ec2tag['Key'].lower():
                    delcount+=1

            if delcount == 0:
                deloninstanceids2.append(ec2in['InstanceId'])
            elif delcount == 1:
                deloninstanceids.append(ec2in['InstanceId'])
            elif delcount > 1:
                print ("delete 설정이 여러개 되어있습니다")

for delinstance in deloninstanceids:
    for ec2tags in ec2tagsinfos:
        if (ec2tags['ResourceType']) == 'instance' and (ec2tags['ResourceId']) == delinstance and (ec2tags['Key']).lower() == ('deleteon').lower():
            deltime = time.mktime(datetime.strptime(ec2tags['Value'], '%Y-%m-%d').timetuple())
            today = time.mktime(datetime.today().timetuple())

            if deltime - today < 0:
                os.system('aws ec2 stop-instances --instance-ids %s' %delinstance)
                print (delinstance + " Stop1")

for delinstance1 in deloninstanceids2:
    os.system('aws ec2 stop-instances --instance-ids %s' %delinstance1)
    print (delinstance1 + " Stop2")
