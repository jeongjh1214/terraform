#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError
import re, datetime
from dateutil.relativedelta import relativedelta

(datetime.datetime.now() - relativedelta(months=1)).strftime('%y%m')

def descriptioncheck(perm):
    description = ['IpRanges','UserIdGroupPairs','Ipv6Ranges','PrefixListIds']
    pattern = re.compile('[0-9]{6}')
    pattern1 = re.compile('^' + (datetime.datetime.now() - relativedelta(months=1)).strftime('%y%m') + '[0-9]{2}')
    all = []
    for i in description:
        for j in perm[i]:
            if 'Description' in j.keys():
                desc = j['Description'].split('_')
                desc2 = j['Description'].split('//')
                if len(desc2) == 1:
                    if len(desc) == 5:
                        createday = desc[2]
                        deleteday = desc[3]
                        a = re.match(pattern1,createday)
                        b = re.match(pattern1,deleteday)
                        if a:
                            j['Name'] = i
                            j['createday'] = 1

                        elif b:
                            j['Name'] = i
                            j['deleteday'] = 1

                        else:
                            continue
                        
                        all.append(j)

                    elif len(desc) > 5 or (len(desc) > 1 and len(desc) < 5):
                        j['Name'] = i
                        j['extra'] = 1
                        all.append(j)
                
                elif len(desc2) > 1:
                    
                
                    


                                                                   
    #return (all)




ec2 = boto3.client('ec2')
test1 = ec2.describe_security_groups()

for i in test1['SecurityGroups']:
    for j in i['IpPermissions']:
        #print (j)
        descriptioncheck(j)
        
    #    # 모두 오픈 되어있음
    #    if j['IpProtocol'] == '-1':
    #        print (f'{j} 값 모두 오픈 되어있습니다')
    #        continue
    #    
    #    if j['IpProtocol'] == 'icmp':
    #        if j['FromPort'] == 0 and j['ToPort'] == -1:
    #            protocol = f'에코 응답'
    #            port = f'해당사항 없음'
    #        
    #        elif j['FromPort'] == -1 and j['ToPort'] == -1:
    #            protocol = f'모두'
    #            port = f'해당사항 없음'
    #        
    #        else:
    #            print (f'{j} icmp 다른 룰 입니다')
    #            continue
#
    #    print (j)
        
        