#!/bin/python3

import sys, json
import boto3
from botocore.exceptions import ClientError
from lib import elbboto 


arn = 'arn:aws:elasticloadlancing:ap-northeast-2:584946075280:listener/app/test/6128197d9dabd7c7/8fe4383c24dc1d92'


print (elbboto.lenrule(arn))
