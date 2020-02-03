#!/bin/python3

import sys, re, os
from urllib import parse
import json
import configparser
import subprocess


mfakey = input("MFA Key를 넣어주세요 \n")

p = re.compile('[0-9]{6}')
ap = re.compile('^arn\:aws\:iam\:\:([0-9]{12})\:mfa\/')

if not p.match(mfakey):
    print ("올바른 mfa를 입력해주세요")
    sys.exit()


config = configparser.ConfigParser()
crepath = os.path.expanduser('~') + "/.aws/credentials"
config.read(crepath)

arn = config["mfa"]["aws_arn_mfa"]


if arn == '':
    print ("credentials 에 mfa arn 입력 바랍니다")
    sys.exit()

elif not ap.match(arn):
    print ("arn 형식이 맞지 않습니다")
    sys.exit()

result = subprocess.run(['aws', 'sts', 'get-session-token', '--profile', 'default', '--serial-number', arn, '--token-code', mfakey], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode != 0:
    print (result.stderr.decode('utf-8').strip('\n'))
    sys.exit()

credentials = json.loads(result.stdout.decode('utf-8'))['Credentials']

config["mfa"]['aws_access_key_id'] = credentials['AccessKeyId']
config["mfa"]['aws_secret_access_key'] = credentials['SecretAccessKey']
config["mfa"]['aws_session_token'] = credentials['SessionToken']

with open(crepath, 'w') as configFile:
    config.write(configFile)

print('MFA 인증 성공하였습니다')