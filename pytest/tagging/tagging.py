#!/bin/python3

import sys
import boto3
import re
import time
from botocore.exceptions import ClientError


#region = 'ap-northeast-2'
#region = 'us-east-1'
#region = 'ap-northeast-1'
#region = 'eu-west-3'
#region = 'ap-southeast-1'

def InsTags(instanceid):
    ec2 = boto3.resource('ec2')
    
    for instance in ec2.instances.filter(InstanceIds=[instanceid]):
        try:
            InsTags = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', instance.tags))
            return (InsTags)
        except KeyError:
            pass

def Volumecheck(response):
    ec2res = boto3.resource('ec2')

    for i in response['Volumes']:
        if i['State'] == 'in-use':
            # 사용중인 Volume 중에서 System Tag 가 없는 Volume 만 진행
            try:
                tagcheck = [a for a in i['Tags'] if a['Key'] == 'System']
            except KeyError:
                tagcheck = None
          
            if tagcheck:
                tagnames = None
                
            else:
                instanceid = [b['InstanceId'] for b in i['Attachments']]
                tagnames = InsTags(instanceid[0])

            if tagnames:
                ec2res.Volume(i['VolumeId']).create_tags(Tags=tagnames)
                print (f"{i['VolumeId']} 볼륨에 {tagnames} 추가 완료하였습니다.")    


def VolumeTagging():
    ec2 = boto3.client('ec2')
    response = ec2.describe_volumes(MaxResults=100)

    Volumecheck(response)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_volumes(MaxResults=100,NextToken=ntoken)
            Volumecheck(response)
        
        except KeyError:
            break


def ENIcheck(response,clenv,id):
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')

    for i in response['NetworkInterfaces']:
        tagcheck = [a for a in i['TagSet'] if a['Key'] == 'System']
        if tagcheck:
            tagname = None
        else:
            try:
                if i['Attachment']:
                    p = re.compile('[0-9]{12}')
                    tagname = None

                    if i['Attachment']['InstanceOwnerId'] == 'amazon-rds':
                        tagname = rdscheck(i['Groups'])
                        
                    elif i['Attachment']['InstanceOwnerId'] == 'amazon-elb':
                        tagname = elbcheck(i['Groups'])
                        if not tagname:
                            tagname = elbcheck2(i['Groups'])
                        else:
                            tagname = None
                            
                    elif p.match(i['Attachment']['InstanceOwnerId']):
                        if i['Attachment']['InstanceOwnerId'] == '020709675181':
                            tagname = [{'Key' : 'System', 'Value' : 'CustomerDataPlatform'},{'Key' : 'Company', 'Value' : 'AP'}, {'Key' : 'Country', 'Value':'KR'},{'Key' : 'STAGE' , 'Value' : ''}]
                            tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=tagname)
                            print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")
                            continue
                        elif i['Attachment']['InstanceOwnerId'] == str(id):
                            tagname = InsTags(i['Attachment']['InstanceId'])
                        else:
                            tagname = redischeck(i['Groups'],id)
                            if not tagname:
                                tagname = None
                    
                    if tagname:
                        tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=tagname)
                        print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")

                    else:
                        tagname = "Resource-ENI " + clenv
                        tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tagname}])
                        print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")

                else:
                    tagname = "Resource-ENI " + clenv
                    tagging = ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tagname}])
                    print (f"{i['NetworkInterfaceId']} eni 태그 {tagname} 등록하였습니다.")
               
            except KeyError:
                pass


def ENITagging(clenv,id):
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')
    response = ec2.describe_network_interfaces(MaxResults=100)

    ENIcheck(response,clenv,id)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_network_interfaces(MaxResults=100,NextToken=ntoken)
            ENIcheck(response,clenv,id)
        
        except KeyError:
            break


def SnapshotTagging():
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=500)
    tagcheckInsert(response)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_snapshots(OwnerIds=['self'],MaxResults=500,NextToken=ntoken)
            tagcheckInsert(response)

        except KeyError:
            break

# Volume 에 따른 Snapshot Tagging
def tagcheckInsert(response):
    ec2res = boto3.resource('ec2')

    for i in response['Snapshots']:
        # System Tag 
        try:
            tagcheck = [a for a in i['Tags'] if a['Key'] == 'System']
        except KeyError:
            tagcheck = None

        if tagcheck:
            tag = None
        else:
            try:
                volume = ec2res.Volume(i.get('VolumeId'))
                insid = volume.attachments[0]['InstanceId']

            except ClientError:
                print (f"볼륨명 {i.get('VolumeId')} 가 없습니다")
                insid = None

            except KeyError:
                print (f"{i.get('SnapshotId')}의 Instance 가 없습니다")
                insid = None

            if insid:
                tag = InsTags(insid)
                if tag:
                    tagging = ec2res.Snapshot(i.get('SnapshotId')).create_tags(Tags=tag)
                    print (f"{insid}를 {i.get('SnapshotId')}에 입력하였습니다")


def amiinscheck(snapshotid):
    ec2 = boto3.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=['self'],SnapshotIds=[snapshotid])

    for i in response['Snapshots']:
        volume = boto3.resource('ec2').Volume(i.get('VolumeId'))
        try:
            return (InsTags(volume.attachments[0]['InstanceId']))
        except ClientError:
            pass 

def amitagcreate():
    ec2 = boto3.client('ec2')
    ec2r = boto3.resource('ec2')
    response = ec2.describe_images(Owners=['self'])

    for i in response['Images']:
        try:
            tagcheck = [a for a in i['Tags'] if a['Key'] == 'System']
        except KeyError:
            tagcheck = None
        
        if tagcheck:
            tag = None
        else:
            for j in i['BlockDeviceMappings']:
                tag = amiinscheck(j['Ebs']['SnapshotId'])
                if tag:
                    tagging = ec2r.Image(i['ImageId']).create_tags(Tags=tag)
                    print (f"{i['ImageId']} 이미지 태그 {tag} 등록 완료하였습니다")
                

def rdscheck(groups):
    ec2 = boto3.client('rds')
    client = ec2.describe_db_instances()
    for i in client['DBInstances']:
        for j in i['VpcSecurityGroups']:
            for group in groups:
                if group['GroupId'] == j['VpcSecurityGroupId']:
                    cl = ec2.list_tags_for_resource(ResourceName=i['DBInstanceArn'])
                    tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagList']))
                    
                    if tag:
                        return (tag)

def elbcheck(groups):
    ec2 = boto3.client('elbv2')
    client = ec2.describe_load_balancers()
    for i in client['LoadBalancers']:
        try:
            for j in i['SecurityGroups']:
                for group in groups:
                    if group['GroupId'] == j:
                        cl = ec2.describe_tags(ResourceArns=[i['LoadBalancerArn']])
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagDescriptions'][0]['Tags']))
                        
                        if tag:
                            return (tag)
        except KeyError:
            pass

def elbcheck2(groups):
    ec2 = boto3.client('elb')
    client = ec2.describe_load_balancers()
    for i in client['LoadBalancerDescriptions']:
        try:
            for j in i['SecurityGroups']:
                for group in groups:
                    if group['GroupId'] == j:
                        cl = ec2.describe_tags(LoadBalancerNames=[i['LoadBalancerName']])
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagDescriptions'][0]['Tags']))
                        
                        if tag:
                            return (tag)
        except KeyError:
            pass

## 일반 RDS 서버 Check
def rdstagcheck(response):
    ec2 = boto3.client('rds')
    for i in response['DBSnapshots']:
        if i['DBInstanceIdentifier']:
            tagcheck = [a for a in ec2.list_tags_for_resource(ResourceName=i['DBSnapshotArn'])['TagList'] if a['Key'] == 'System']
            if tagcheck:
                tagcheck = None
                
            else:
                try:
                    res = ec2.describe_db_instances(DBInstanceIdentifier=i['DBInstanceIdentifier'])
                    if res['DBInstances']:
                        resource = res['DBInstances'][0]['DBInstanceArn']
                        cl = ec2.list_tags_for_resource(ResourceName=resource)
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagList']))
                        
                        if tag:
                            tagging = ec2.add_tags_to_resource(ResourceName=i['DBSnapshotArn'],Tags=tag)
                            print (f"{i['DBSnapshotArn']}에 {tag} 등록 완료하였습니다")
            
                except ClientError:
                    pass

## Cluster RDS 서버 Check                
def rdstagcheck2(response):
    ec2 = boto3.client('rds')
    for i in response['DBClusterSnapshots']:
        if i['DBClusterIdentifier']:
            tagcheck = [a for a in ec2.list_tags_for_resource(ResourceName=i['DBClusterSnapshotArn'])['TagList'] if a['Key'] == 'System']
            if tagcheck:
                tagcheck = None
                
            else:
                try:
                    res = ec2.describe_db_clusters(DBClusterIdentifier=i['DBClusterIdentifier'])
                    if res['DBClusters']:
                        resource = res['DBClusters'][0]['DBClusterArn']
                        cl = ec2.list_tags_for_resource(ResourceName=resource)
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagList']))
                        
                        if tag:
                            tagging = ec2.add_tags_to_resource(ResourceName=i['DBClusterSnapshotArn'],Tags=tag)
                            print (f"{i['DBClusterSnapshotArn']}에 {tag} 등록 완료하였습니다")
            
                except ClientError:
                    pass  

# 일반 RDS Snapshot Tagging Check
def rdssnapshot():
    ec2 = boto3.client('rds')
    response = ec2.describe_db_snapshots(MaxRecords=100)
    rdstagcheck(response)
    
    while True:
        try:
            marker = response['Marker']
            response = ec2.describe_db_snapshots(Marker=marker,MaxRecords=100)
            rdstagcheck(response)
        except KeyError:
            break

# Cluster RDS Snapshot Tagging Check            
def rdssnapshot2():
    ec2 = boto3.client('rds')
    response = ec2.describe_db_cluster_snapshots(MaxRecords=100)
    rdstagcheck2(response)
    
    while True:
        try:
            marker = response['Marker']
            response = ec2.describe_db_cluster_snapshots(Marker=marker,MaxRecords=100)
            rdstagcheck(response)
        except KeyError:
            break

# ec2 기준 모든 System Tag 별 Company, Country, STAGE Tagging 값 가져오기
def Alltags():
    client = boto3.resource('ec2')
    Alltags = {}

    for instance in client.instances.filter(MaxResults=500):
        try:
            SystemTag = list(filter(lambda tag: tag['Key'] == 'System', instance.tags))[0]['Value']
            InsTags = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', instance.tags))
            Alltags[SystemTag] = InsTags 

        except IndexError:
            print (str(instance) + ' IndexError')
            pass

        except TypeError:
            print (str(instance) + ' TypeError')

    return (Alltags)

#강제 Tagging
def securitytagging():
    alltags = Alltags()
    ec2 = boto3.client('ec2')
    client = ec2.describe_security_groups()

    for i in client['SecurityGroups']:
        ec2res = boto3.resource('ec2')
        try:
            sgres = [a['Value'] for a in ec2res.SecurityGroup(i['GroupId']).tags if a['Key'] == 'System']

        except TypeError:
            sgres = None

        if sgres:
            try:
                systemcheck = alltags[sgres[0]]

            except KeyError:
                    print (f"{i['GroupId']} SG System 태그 {sgres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2res.SecurityGroup(i['GroupId']).create_tags(Tags=systemcheck)

#강제 Tagging
def networktagging():
    alltags = Alltags()
    ec2 = boto3.client('ec2')
    client = ec2.describe_network_interfaces()

    for i in client['NetworkInterfaces']:
        ec2res = boto3.resource('ec2')
        try:
            netres = [a['Value'] for a in ec2res.NetworkInterface(i['NetworkInterfaceId']).tag_set if a['Key'] == 'System']

        except TypeError:
            netres = None

        if netres:
            try:
                systemcheck = alltags[netres[0]]
            except KeyError:
                    print (f"{i['NetworkInterfaceId']} ENI System 태그 {netres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None
            if systemcheck:
                ec2res.NetworkInterface(i['NetworkInterfaceId']).create_tags(Tags=systemcheck)

#강제 Tagging
def elbtagging():
    alltags = Alltags()
    ec2 = boto3.client('elb')
    client = ec2.describe_load_balancers()

    for i in client['LoadBalancerDescriptions']:
        try:
            elbres = [a['Value'] for a in ec2.describe_tags(LoadBalancerNames=[i['LoadBalancerName']])['TagDescriptions'][0]['Tags'] if a['Key'] == 'System']

        except TypeError:
            elbres = None

        if elbres:
            try:
                systemcheck = alltags[elbres[0]]

            except KeyError:
                    print (f"{i['LoadBalancerName']} ELB2 System 태그 {elbres[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2.add_tags(LoadBalancerNames=[i['LoadBalancerName']],Tags=systemcheck)

#강제 Tagging
def elb2tagging():
    alltags = Alltags()
    ec2 = boto3.client('elbv2')
    client = ec2.describe_load_balancers()

    for i in client['LoadBalancers']:
        try:
            elb2res = [a['Value'] for a in ec2.describe_tags(ResourceArns=[i['LoadBalancerArn']])['TagDescriptions'][0]['Tags'] if a['Key'] == 'System']
        except TypeError:
            elb2res = None

        if elb2res:
            try:
                systemcheck = alltags[elb2res[0]]

            except KeyError:
                    print (f"{i['LoadBalancerArn']} ELB2 System 태그 {elb2res[0]} 와 매칭되는 System 키가 없습니다")
                    systemcheck = None

            if systemcheck:
                ec2.add_tags(ResourceArns=[i['LoadBalancerArn']],Tags=systemcheck)

#강제 Tagging
def apigatewaytagging():
    client = boto3.client('apigateway')
    for i in client.get_rest_apis()['items']:
        apiid = (i['id'])
        arnres = f'arn:aws:apigateway:{region}::/restapis/{apiid}'
        updatetags = client.tag_resource(
            resourceArn=arnres,
            tags={'Company' : 'AP', 'Country' : 'KR', 'Service' : '', 'STAGE' : 'ETC'}
        )

        print (updatetags)

#강제 Tagging
def sagemakertagging():
    sage = boto3.client('sagemaker', region_name='ap-northeast-2')
    train = sage.list_training_jobs(MaxResults=100)
    for i in train['TrainingJobSummaries']:
        resarn = i['TrainingJobArn']
        tags = sage.add_tags(ResourceArn=resarn,Tags=[{'Key' : 'Country', 'Value' : 'KR'},{'Key' : 'Company', 'Value' : 'AP'},{'Key' : 'Sytem', 'Value' : 'DigitalRnD Recsys'},{'Key' : 'STAGE', 'Value' : 'PRD'}])
        print (resarn)
        time.sleep(1)

    while True:
        try:
            check = train['NextToken']
            train2 = sage.list_training_jobs(NextToken=check,MaxResults=100)
            for j in train2['TrainingJobSummaries']:
                resarn2 = j['TrainingJobArn']
                tags2 = sage.add_tags(ResourceArn=resarn2,Tags=[{'Key' : 'Country', 'Value' : 'KR'},{'Key' : 'Company', 'Value' : 'AP'},{'Key' : 'Sytem', 'Value' : 'DigitalRnD Recsys'},{'Key' : 'STAGE', 'Value' : 'PRD'}])
                print (resarn2)
                time.sleep(1)
        except KeyError:
            sys.exit()

#강제 Tagging
def sagemakertagging2():
    sage = boto3.client('sagemaker', region_name='ap-northeast-2')
    train = sage.list_endpoint_configs(MaxResults=100)
    for i in train['EndpointConfigs']:
        resarn = i['EndpointConfigArn']
        tag = sage.add_tags(ResourceArn=resarn,Tags=[{'Key' : 'Country', 'Value' : 'KR'},{'Key' : 'Company', 'Value' : 'AP'},{'Key' : 'Sytem', 'Value' : 'DigitalRnD Recsys'},{'Key' : 'STAGE', 'Value' : 'PRD'}])
        print (resarn)
        time.sleep(1)

def start(stage,idnumber):
    SnapshotTagging()
    rdssnapshot()
    rdssnapshot2()
    ENITagging(stage,idnumber)
    sgtagging(stage,idnumber)

def sectagcheck(response,clenv,id):
    ec2res = boto3.resource('ec2')

    for i in response['SecurityGroups']:
        tagcheck = [a for a in ec2res.SecurityGroup(i['GroupId']).tags if a['Key'] == 'System']
        if tagcheck:
            tagnames = None
        else:
            try:
                groupname = i['GroupId']
                groupid = {}
                groupid['GroupId'] = groupname
                
                ecins = ec2.describe_instances(Filters=[{'Name':'network-interface.group-id', 'Values':[groupname]}])
                if ecins['Reservations']:
                    for k in ecins['Reservations']:
                        instance = [a['InstanceId'] for a in k['Instances']]
                        if InsTags(instance[0]):
                            tag = InsTags(instance[0])
                            if tag:
                                tagging = ec2res.SecurityGroup(i['GroupId']).create_tags(Tags=tag)
                                print (i['GroupId'],tag)
                else:
                    if rdscheck([groupid]):
                        tag = rdscheck([groupid])
                        
                    elif elbcheck([groupid]):
                        tag = elbcheck([groupid])
                        
                    elif elbcheck2([groupid]):
                        tag = elbcheck2([groupid])
                    
                    elif redischeck([groupid],id):
                        tag = redischeck([groupid],id)
                        
                    if tag:
                            tagging = ec2res.SecurityGroup(i['GroupId']).create_tags(Tags=tag)
                            print (i['GroupId'],tag)
                    else:
                        tag = 'Resource-SG ' + clenv
                        test1 = ec2res.SecurityGroup(i['GroupId']).create_tags(Tags=[{'Key' : 'System', 'Value' : tag}])
                        print (i['GroupId'],tag)
            
            except KeyError:
                pass            

def redischeck(groups,id):
    ec2 = boto3.client('elasticache')
    response = ec2.describe_cache_clusters()
    for i in response['CacheClusters']:
        try:
            for j in i['SecurityGroups']:
                for group in groups:
                    if group['GroupId'] == j['SecurityGroupId']:
                        region = i['PreferredAvailabilityZone'][:-1]
                        redisid = i['CacheClusterId']
                        redisarn = f'arn:aws:elasticache:{region}:{id}:cluster:{redisid}'
                        cl = ec2.list_tags_for_resource(ResourceName=redisarn)
                        tag = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Company' or tag['Key'] == 'Country' or tag['Key'] == 'STAGE', cl['TagList']))

                        if tag:
                            return (tag)

def sgtagging(clenv,id):
    ec2 = boto3.client('ec2')
    ec2res = boto3.resource('ec2')
    response = ec2.describe_security_groups(MaxResults=100)

    sectagcheck(response,clenv,id)

    while True:
        try:
            ntoken = response['NextToken']
            response = ec2.describe_security_groups(MaxResults=100,NextToken=ntoken)
            sectagcheck(response,clenv,id)
        
        except KeyError:
            break
    
    
def lambda_handler(event, context):

    #amitagcreate()
    #createSnapshotTag()
    #enitagcreate("APPRD")
    #sgtagging("APPRD")
    #rdssnapshot()

    ### System 기반 Tagging 사용
    #volumtagging()
    #securitytagging()
    #networktagging()
    #elbtagging()
    #elb2tagging()
    #apigatewaytagging()
    #sagemakertagging2()

    #최신버전 크론용
    
    #start(stage,idnumber)
    #VolumeTagging()