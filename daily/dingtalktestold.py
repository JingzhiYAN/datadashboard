#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,json
with open('credentials.txt', 'r') as file:
  lines = file.readlines()
  token = lines[6].strip()

webhook = token
data="COCO testdata1"
headers = {'Content-Type': 'application/json'}
data={
  "msgtype": "text",
  "text": {"content": data},
  "at": {"atMobiles": [110,120] },
  "isAtAll": True
}
res = requests.post(webhook,data=json.dumps(data),headers=headers)
