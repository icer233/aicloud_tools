# -*- coding: utf-8 -*-
import requests
import json

screenRecordListUrl = "https://www.aiwenyun.cn/yxt/servlet/antiScreenRecord/nct/getScreenRecordList"
headers = {
    "Host": "www.aiwenyun.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ai_client/1.07.126 Chrome/89.0.4389.128 Electron/12.0.18 Safari/537.36",
    "platform": "ai",
    "access-token": "previewToken",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Language": "zh-CN",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "23"
}
payload = {
   "os": "windows",
   "subOrgId" : 12581
}

screenRecordList = requests.post(screenRecordListUrl, headers=headers, json=payload, verify=False).json()["obj"]
with open('./screenRecord_list.json', 'w', encoding='utf-8') as f:
        json.dump(screenRecordList, f, ensure_ascii=False, indent=4)