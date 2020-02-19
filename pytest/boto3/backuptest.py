#!/bin/python3

import boto3
import datetime
import time
import os, sys



ec2 = boto3.resource('ec2')



print("\n\nAWS snapshot backups starting at %s" % datetime.datetime.now())
instances = ec2.instances.filter(MaxResults=500)

for instance in instances:
    
    instance_name = list(filter(lambda tag: tag['Key'] == 'Name' or tag['Key'] == 'System', instance.tags))[0]['Value']
    tags = list(filter(lambda tag: tag['Key'] == 'System' or tag['Key'] == 'Name' or tag['Key'] == 'Company' or tag['Key'] == 'STAGE' or tag['Key'] == 'Name', instance.tags))

    print (tags)
    sys.exit()
    
    print("instance_name [%s]" % instance_name)

    for volume in ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance.id]}]):
        description = 'scheduled-%s.%s-%s' % (instance_name, volume.volume_id, 
            datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        
        response = volume.create_snapshot(Description=description, VolumeId=volume.volume_id)    
        
        if response:
            print("Snapshot created with description [%s]" % description)
            ec2.create_tags( Resources=[response.snapshot_id],
            Tags=tags)
            #snapshot = ec2.Snapshot(response.snapshot_id)
            #snapshot.create_tags(Tags=[{'Key': 'Name','Value': description}])
        
        #for snapshot in volume.snapshots.all():
        #    retention_days = int(os.environ['retention_days'])
        #    if snapshot.description.startswith('scheduled-') and ( datetime.datetime.now().replace(tzinfo=None) - snapshot.start_time.replace(tzinfo=None) ) > datetime.timedelta(days=retention_days):
        #        print("\t\tDeleting snapshot [%s - %s]" % ( snapshot.snapshot_id, snapshot.description ))
        #        snapshot.delete()
    
        time.sleep(1)
        
print("\n\nAWS snapshot backups completed at %s" % datetime.datetime.now())
