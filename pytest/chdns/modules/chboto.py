#!/bin/python3

import sys
import boto3
from botocore.exceptions import ClientError

client = boto3.client('route53')

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
                    'ResourceRecords' : [{'Value' : '111.111.11.1'}]
                }
            }
        ]
    }
)

print (response)
            
