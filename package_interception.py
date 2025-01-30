import os
import sys
import winreg
import subprocess
import asyncio
import keyboard  # 用于监听键盘事件
from mitmproxy import http, options
from mitmproxy.tools import dump
import threading  # 用于在单独线程中运行键盘监听

# 配置参数
PROXY_PORT = 8888
TARGET_URL = "https://www.aiwenyun.cn/yxt/servlet/antiScreenRecord/nct/getScreenRecordList"

class SilentInterceptor:
    def request(self, flow: http.HTTPFlow):
        if (
            flow.request.method == "POST" 
            and flow.request.pretty_url == TARGET_URL
        ):
            print(f"[拦截成功] 已阻止请求：{flow.request.url}")  # 唯一可见的输出
            flow.response = http.Response.make(
                200,
                b'[{}]',
                {"Content-Type": "application/json"}
            )

class WindowsProxyManager:
    def __init__(self):
        self.original_enable = None
        self.original_server = None

    def __enter__(self):
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_READ
        ) as key:
            self.original_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
            self.original_server = winreg.QueryValueEx(key, "ProxyServer")[0]
        
        self._set_proxy(1, f"127.0.0.1:{PROXY_PORT}")
        print("[系统代理] 已设置为本地代理")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._set_proxy(0, f"127.0.0.1:{PROXY_PORT}")
        print("[系统代理] 已关闭系统代理，可关闭程序")

    def _set_proxy(self, enable, server):
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_WRITE
        ) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, enable)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, server)
            winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "<local>")

def install_certificate():
    """安装mitmproxy证书到系统存储"""
    cert_path = os.path.expanduser(r"~\.mitmproxy\mitmproxy-ca-cert.cer")
    if not os.path.exists(cert_path):
        print("[证书错误] 未找到证书文件，请先运行一次mitmdump生成证书")
        sys.exit(1)
    
    cmd = f'certutil -f -addstore "Root" "{cert_path}"'
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print("[证书] 已成功安装到系统信任存储")
    except subprocess.CalledProcessError as e:
        print(f"[证书错误] 安装失败: {e.stderr.decode('gbk')}")
        sys.exit(1)

def check_admin():
    """检测管理员权限"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

async def start_proxy():
    """静默模式代理服务"""
    opts = options.Options(
        listen_port=PROXY_PORT,
        ssl_insecure=True,
        upstream_cert=False,
    )
    
    master = dump.DumpMaster(
        opts,
        with_termlog=False,  # 禁用终端日志
        with_dumper=False    # 禁用流量转储
    )
    master.addons.add(SilentInterceptor())
    
    try:
        await master.run()
    except KeyboardInterrupt:
        master.shutdown()

def close_proxy_and_exit():
    """关闭代理并退出程序"""
    print("[系统代理] 正在关闭代理服务...")
    # 调用__exit__方法，恢复系统代理设置
    global proxy_manager
    proxy_manager.__exit__(None, None, None)
    sys.exit()

def listen_for_exit():
    """监听Ctrl+Q键退出程序"""
    print("[系统就绪] 代理服务运行中 (按 Ctrl+Q 关闭)")
    keyboard.add_hotkey('ctrl+q', close_proxy_and_exit)  # 当检测到Ctrl+Q时调用close_proxy_and_exit()
    keyboard.wait('esc')  # 等待ESC键被按下，可以退出键盘监听线程

def main():
    global proxy_manager
    proxy_manager = WindowsProxyManager()

    with proxy_manager:
        if sys.version_info >= (3, 8) and sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # 启动监听线程
        listener_thread = threading.Thread(target=listen_for_exit)
        listener_thread.daemon = True  # 使得程序退出时自动关闭该线程
        listener_thread.start()
        
        # 静默启动
        print("[系统就绪] 代理服务运行中，仅显示拦截信息...")
        asyncio.run(start_proxy())

if __name__ == "__main__":
    main()
