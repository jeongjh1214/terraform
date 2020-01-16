#!/bin/python3

import json, os, sys
from datetime import datetime
import time


command = os.popen("aws ec2 describe-instances --query Reservations[*]")
command2 = os.popen("aws ec2 describe-tags --query Tags[*]")

ec2infos = json.load(command)
ec2tagsinfos = json.load(command2)

b = [a['Instances'] for a in ec2infos]
#print (b[0][0].keys())
d = [(c[0]['Tags'],c[0]['InstanceId']) for c in b if 'Tags' in c[0].keys()]

#tagdata = [x['InstanceId'] for ec2info in ec2infos for x in ec2info['Instances'] if 'Tags' in x.keys() else None]
tagdata = [x['InstanceId'] for ec2info in ec2infos if 'Tags' in x.keys() else None for x in ec2info['Instances']]
print (tagdata)

# deleteon 있는 서버
#deloninstanceids = []
#
## deleteon 없는 서버
#deloninstanceids2 = []
#
#for ec2info in ec2infos:
#    ec2ins = ec2info['Instances']
#    for ec2in in ec2ins:
#        if 'Tags' not in ec2in.keys():
#            print ("no tags " + ec2in['InstanceId'])
#        else:
#            delcount = 0
#            for ec2tag in ec2in['Tags']:
#                if "DeleteOn".lower() in ec2tag['Key'].lower():
#                    delcount+=1
#
#            # tags 에서 deleteon 태그 여부 확인, 여러개 있을 경우에는 예외상태로 설정
#            if delcount == 0:
#                deloninstanceids2.append(ec2in['InstanceId'])
#            elif delcount == 1:
#                deloninstanceids.append(ec2in['InstanceId'])
#            elif delcount > 1:
#                print ("delete 설정이 여러개 되어있습니다")
#
#
## deleteon 설정된 서버들에 대해서 처리
#for delinstance in deloninstanceids:
#    for ec2tags in ec2tagsinfos:
#        if (ec2tags['ResourceType']) == 'instance' and (ec2tags['ResourceId']) == delinstance and (ec2tags['Key']).lower() == ('deleteon').lower():
#            deltime = time.mktime(datetime.strptime(ec2tags['Value'], '%Y-%m-%d').timetuple())
#            today = time.mktime(datetime.today().timetuple())
#
#            if deltime - today < 0:
#                os.system('aws ec2 stop-instances --instance-ids %s' %delinstance)
#                print (delinstance + " Stop1")
#
#
## tags 가 전혀 없는 서버들에 대해 처리
#for delinstance1 in deloninstanceids2:
#    os.system('aws ec2 stop-instances --instance-ids %s' %delinstance1)
#    print (delinstance1 + " Stop2")
