#!/bin/python3

import os,shutil
import configparser

crepath = os.path.expanduser('~') + "/.aws/credentials"

if os.path.exists(crepath) and os.path.getsize(crepath):
    shutil.copy2(crepath,crepath + "_backup")
    config = configparser.ConfigParser()
    config.read(crepath)
    requireOp = ['aws_arn_mfa', 'aws_access_key_id', 'aws_secret_access_key', 'aws_session_token', 'region']

    if config.has_section("mfa"):
              
        ConfigOp = config.options("mfa")
        extraRequireOp = list(set(requireOp) - set(ConfigOp))

        if len(extraRequireOp) > 0:
            for i in extraRequireOp:
                config.set("mfa",i,"")

            with open(crepath, 'w') as configFile:
                config.write(configFile)
                print ("success")

    else:
        config.add_section('mfa')
        arn = input("MFA arn을 넣어주세요 \n")

        for i in requireOp:
            config.set("mfa",i,"")

        config.set("mfa","aws_arn_mfa",arn)

        with open(crepath, 'w') as configFile:
            config.write(configFile)
            print ("success")