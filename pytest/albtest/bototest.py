#!/bin/python3

import sys, json
import boto3
from botocore.exceptions import ClientError
from lib import elbboto 


arn = 'arn:aws:elasticloadbalancing:ap-northeast-2:779475221336:listener/app/alb-an2-jaehoon-bototest/03690c817c2afce0/36817b103e314794'
sourcefile = "test.txt"
targetfile = "target.txt"
startnum = 1

elbboto.makealbrule(arn,sourcefile,targetfile,startnum)
