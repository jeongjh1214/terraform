#!/bin/python3

from module import gasheet, botolib


cellcount = 2

allinsmap = botolib.allinstance_list()
regions = list(allinsmap.keys())

for region in regions:
    for insid in allinsmap[region]:
        tagdata = botolib.fullname_check(insid[0],region)
        if tagdata is not False:
            for tags in tagdata:
                if 'fullname' in tags['Key']:
                    name = tags['Value']
                elif 'Name' in tags['Key']:
                    resource_name = tags['Value']

            gasheet.insert_data('A' + str(cellcount),name)
            gasheet.insert_data('B' + str(cellcount),region)
            gasheet.insert_data('C' + str(cellcount),'EC2')
            gasheet.insert_data('D' + str(cellcount),resource_name)
            gasheet.insert_data('E' + str(cellcount),insid[1])
            gasheet.insert_data('F' + str(cellcount),insid[0])
            cellcount += 1

