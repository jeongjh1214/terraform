#!/bin/python3

from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import requests
import xml.etree.ElementTree as ET
import datetime

def holidaycheck():
    nowYear = datetime.datetime.now().strftime("%Y")
    nowMonth = datetime.datetime.now().strftime("%m")
    nowDay = datetime.datetime.now().strftime("%d")
    
    allday = str(nowYear) + str(nowMonth) + str(nowDay)

    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
    srvk = 'MTiaDMPrbA1G6%2BxpDgk%2FgjG0Ps1kxIzeRnrFb04ULj1D4L9IS81UbvnM9VZBTtdfFOsxeJdMilF6RLHnf3MIcQ%3D%3D'
    queryParams = '?ServiceKey=' + srvk + '&solYear=' + nowYear + '&solMonth=' + nowMonth
    
    fullurl = url + queryParams
    requests.get(fullurl)
    response_body = urlopen(fullurl).read()
    
    tree = ET.fromstring(response_body)
    
    cnt = 0
    
    for i in tree.find('body')[0]:
        if allday in i.find('locdate').text:
            cnt += 1
    
    return (cnt)
