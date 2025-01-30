from mitmproxy import http
import json

def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url == "https://www.aiwenyun.cn/yxt/servlet/antiScreenRecord/nct/getScreenRecordList":
        flow.response.text = json.dumps({
            "code": 0,
            "obj": [],
            "execTime": 8})