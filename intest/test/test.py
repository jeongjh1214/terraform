#!/bin/python3

import yaml

filename = yaml.load(open('all.yml','r'),Loader=yaml.FullLoader)

#print (filename)
for a in filename:
    for b in a['tasks']:
        if b['name'] == 'httpd':
            print (b)
#for a in filename:
#    print (a['tasks'])

#data = {'hosts' : sysenv, 'gather_facts': False, 'tasks' : 


#savetest = open('test.yml','w')
#yaml.dump(filename,savetest)
#print (yaml.dump(filename))


