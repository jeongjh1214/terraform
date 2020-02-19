#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError

def changeIp(ipAddr):
    client = boto3.client('route53')

    ipres = client.list_resource_record_sets(
    HostedZoneId = 'Z277UKQU2HBLK4',
    StartRecordName = 'test.hdh.kr',
    StartRecordType = 'A'
    )
    
    dnsip = ipres['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

    if ipAddr != dnsip:

        response = client.change_resource_record_sets(
            HostedZoneId='Z277UKQU2HBLK4',
            ChangeBatch = {
                'Changes': [
                    {
                        'Action' : 'UPSERT',
                        'ResourceRecordSet' : {
                            'Name' : 'test.hdh.kr',
                            'Type' : 'A',
                            'TTL' : 60,
                            'ResourceRecords' : [{'Value' : ipAddr}]
                        }
                    }
                ]
            }
        )

def lambda_handler (event, context):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance('i-010fe7c08ed5e0708')
    
    if instance.state['Code'] == 16:
        changeIp(instance.public_ip_address)