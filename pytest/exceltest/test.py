#!/bin/python3

from modules import excel, ec2infos 

# 엑셀파일 생성
efile = excel.MakeExcel("ec2test")
efile.newfile()

for tag in ec2infos.alltags():
    if len(tag) > 30:
        tag = tag[:25]

    efile.createsheet(tag)
    instancedata = ec2infos.ec2infos('ap-northeast-2',tag)
    
    # No, 환경, 지역, Hostname, AMI, Instance Type, Private IP, Root Volume(GB), IAM role, Data Volume(GB), Swap Space(GB)
    instancehead = ['No','환경','지역','Hostname','AMI','Instance Type','Private IP','Root Volume(GB)','IAM role','Data Volume(GB)','Swap Space(GB)']
    efile.insertdata(tag,'A1',instancehead,mode='all')
    
    for i in instancedata:
        efile.insertdata(tag,'A2',i,mode='all')
    
    efile.insertdata(tag,'A3',[''],mode='all')

    autodata = ec2infos.asinfos(tag)
    # Auto Scaling 명, 런치 Config명, Increase 정책, Decrease 정책, 기타
    autohead = ['Auto Scaling명','런치 Config명', 'Increase 정책', 'Descrease 정책', '기타']
    efile.insertdata(tag,'A4',autohead,mode='all')

    if autodata == False:
        pass
    else:
        for j in autodata:
            efile.insertdata(tag,'A5',j,mode='all')

    # No, ELB이름, 구분, 통신 Type, Port // target group name, Hostname, Port
    




    

