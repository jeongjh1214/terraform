#!/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        ]
json_file_name = './module/config/resolute-land-265707-e9987132aa5c.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1_AJ20toRjr5K6vRaRjbxw9hZjuy-o8ayhPuLM2W6pGU/edit#gid=0'
# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')

def insert_data(cell, context):
    worksheet.update_acell(cell,context)

