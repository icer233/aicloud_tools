# 爱问云工具箱

## 简介
爱问云工具箱是一个功能丰富的工具集，主要用于处理与爱问云相关的任务。它可以实现诸如回放视频下载、一键反反截屏、修改部分界面内容、阻止反录屏、反虚拟机等功能

## 安装与使用

### 安装依赖
在项目根目录下，使用以下命令安装所需的依赖库：
```sh
pip install -r requirements.txt
```

### 运行代理劫持服务
要启动代理劫持服务，直接运行`package_interception.py`文件：
```sh
python package_interception.py
```

### 运行程序

若要运行主程序，直接运行`main.py`文件：
```shell
python main.py
```

## 注意事项
- **管理员权限**：部分功能（如系统代理设置、证书安装）需要管理员权限，请确保以管理员身份运行相关脚本。
- **代理劫持服务操作流程**：要先关闭其他代理，**以管理员身份**启动服务，然后运行爱问云。登陆爱问云后出现劫持提示即为成功。
- **证书问题**：在使用代理服务前，请确保已经用mitmdump安装mitmproxy证书，否则可能会出现SSL验证错误。
- **使用代理后无法上网**：前往“设置”-“网络和Internet”-“代理”-“手动设置代理”-“设置”-“使用代理服务器”，将其关闭，“保存”即可。

## 贡献指南
如果你对该项目感兴趣并希望做出贡献，可以按照以下步骤进行：
1. 克隆仓库到本地：
```sh
git clone https://github.com/icer233/aicloud_tools.git
```
2. 创建并切换到新的分支：
```sh
git checkout -b main
```
3. 进行代码修改和功能添加。
4. 提交并推送你的更改：
```sh
git add .
git commit -m "你的提交信息"
git push origin <分支名称>
```
5. 创建一个Pull Request，详细描述你的更改内容。

## 联系信息
如果你在使用过程中遇到任何问题或有任何建议，可以通过以下方式联系我们：
- 邮箱：tommydai0909@163.com

- Gitee：[Alex omega/get_aicloud](https://gitee.com/alex-omega/get_aicloud/)