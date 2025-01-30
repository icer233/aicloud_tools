import requests, hashlib,os

UA = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ai_client/1.07.123 Chrome/89.0.4389.128 Electron/12.0.18 Safari/537.36"

def create_path(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def download_m3u8_segments(m3u8_url, name, output_dir):
    # 发送 HTTP 请求获取 M3U8 文件内容
    headers = {
        "user-agent": UA
    }
    response = requests.get(m3u8_url, headers=headers)
    m3u8_content = response.text
    # 保存 M3U8 文件到本地
    with open(os.path.join(output_dir, name + ".m3u8"), 'w') as f:
        f.write(m3u8_content)

# doLogin 登录获得 access-token 
def getAccessToken(name, passwd, hashed = False):
    login_url = "https://www.aiwenyun.cn/custom/usr/doLogin"
    login_headers = {
        "host": "www.aiwenyun.cn",
        "user-agent": UA,
        "platform": "ai",
        "access-token": "previewToken",
        "content-type": "application/json",
        "accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN",
    }
    if not hashed:
        passwd = hashlib.md5(passwd.encode()).hexdigest()
    login_payload = {
        "rawName": name,
        "name": name,
        "passwd": passwd,
        "loginName": name,
        "role": 1,
        "osInfo": "13th Gen Intel(R) Core(TM) i7-13700H 31.73G 19.99G Windows_NT10.0.22631 ia32 ",
        "version": "12.0.18_5.51.182",
        "deviceId": "windows-a7f8caaa-7a77-4468-a93f-9b8359857ff7",
        "deviceName": "Alex",
        "systemInfo": "10.0.22631 ia32 1.07.123",
        "clientVersion": "5.51.182",
    }

    response = requests.post(login_url, headers=login_headers, json=login_payload)

    access_token = response.json()["obj"]["access_token"]
    return access_token

# 获得回放列表
def getRecordList(access_token):
    reclist_url = "https://www.aiwenyun.cn/liveclassgo/api/v1/history/listRecord"
    reclist_headers = {
        "host": "www.aiwenyun.cn",
        "user-agent": UA,
        "platform": "ai",
        "access-token": access_token,
        "content-type": "application/json",
        "accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN",
    }
    reclist_payload = {
        "dateFrom": 1300000000000,
        "dateTo":   1899999999000,
        "indexStart": 0,
        "pageSize": 50000
    }

    response = requests.post(reclist_url, headers=reclist_headers, json=reclist_payload, proxies={"http": None, "https": None})

    record_list = list(response.json()["obj"]["list"])
    # print(record_list)
    return record_list

# if __name__ == '__main__':
#     passwd = "zsq20100806"
#     name = "jhpyS01594@al"
#     output_dir = "./output_m3u8/"
#     name_dict = {}
#     access_token = getAccessToken(name, passwd)
#     record_list = getRecordList(access_token)
#     create_path(output_dir)

#     # 同步下载每个 m3u8 文件
#     for record_ in record_list:
#         addr = "https://filecdn.plaso.cn/liveclass/plaso/" + record_["fileCommon"]["location"] + "/ts1/t.m3u8"
#         name = record_["shortDesc"]
#         try:
#             name_dict[name] += 1
#         except: 
#             name_dict[name] = 0
#         print(name, ": ", addr)
#         download_m3u8_segments(addr, name, output_dir)
