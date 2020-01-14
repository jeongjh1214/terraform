#!/bin/python3

import json, os
from datetime import datetime
import time

command = os.popen("aws ec2 describe-tags --query Tags[*]")
command2 = os.popen("aws ec2 describe-instance-status --query InstanceStatuses[*]")

a = json.load(command)
b = json.load(command2)

for i in a:
    if (i['ResourceType']) == 'instance' and (i['Key']).lower() == ('deleteon').lower():
        bb = time.mktime(datetime.strptime(i['Value'], '%Y-%m-%d').timetuple())
        today = time.mktime(datetime.today().timetuple())

        if bb-today < 0:
            instanceid = (i['ResourceId'])

            for j in b:
                if j['InstanceId'] == instanceid and j['InstanceState']['Name'] == 'running':
                    os.system('aws ec2 stop-instances --instance-ids %s' %instanceid)
                    print (instanceid + " Stop")
