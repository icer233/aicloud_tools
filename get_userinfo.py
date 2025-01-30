import getpass, os, json
username = getpass.getuser()

dbpath = "C:\\Users\\%s\AppData\\Roaming\\ai_client\\Local Storage" % username

def get_all_files():
    file_list = []
    for root, _, files in os.walk(dbpath):
        for file in files:
            if file.endswith(".ldb"):
                file_list.append(os.path.join(root, file))
    return file_list

files = get_all_files()
# for file in files:
#     print(file)
import re

def check_substring(binary_str):
    # 编译正则表达式模式，匹配特定的JSON结构
    pattern = re.compile(
        rb'\[\{'        # 匹配 [{
        rb'"env":"[^"]*"'       # 匹配 "env":"..."
        rb',"name":"[^"]*"'     # 匹配 ,"name":"..."
        rb',"password":"[^"]*"' # 匹配 ,"password":"..."
        rb',"mytype":[^,}]*'    # 匹配 ,"mytype":数值或其他类型（非逗号、非}的字符）
        rb',"origin":"[^"]*"'   # 匹配 ,"origin":"..."
        rb'\}'        # 匹配 }]
    )
    return bool(pattern.search(binary_str))

def extract_credentials(binary_str):
    # 匹配目标JSON结构并捕获整个JSON数组
    pattern = re.compile(
        rb'\[\{'                                      # 匹配 [{
        rb'"env":"[^"]*"'                             # 匹配 "env":"..."
        rb',"name":"([^"]*)"'                         # 捕获name的值
        rb',"password":"([^"]*)"'                     # 捕获password的值
        rb',"mytype":[^,}]*'                          # 匹配mytype字段
        rb',"origin":"[^"]*"'                         # 匹配origin字段
        rb'\}\]'                                      # 匹配 }]
    )
    
    match = pattern.search(binary_str)
    if not match:
        return None, None  # 未找到匹配项
    
    # 直接通过正则分组提取name和password的字节值
    name_bytes = match.group(1)
    password_bytes = match.group(2)
    
    # 将字节解码为字符串（假设字段内容是UTF-8编码）
    try:
        name = name_bytes.decode('utf-8')
        password = password_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # 若UTF-8解码失败，尝试更宽松的Latin-1解码
        name = name_bytes.decode('latin-1')
        password = password_bytes.decode('latin-1')
    
    return name, password

def get_userinfo():
    un = ""
    pw = ""
    has = False
    for file in files:
        with open(file, "rb") as f:
            rf = f.read()
            has_info = check_substring(rf)
            if has_info:
                has = True
                un, pw = extract_credentials(rf)
            break
    if not has:
        return False
    return un, pw