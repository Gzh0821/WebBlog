# A Simple Django WebBlog

 一个简易的，支持markdown语法的博客系统。可零基础搭建，易于复现与修改！

基于`python 3.10`，`django 4.0`和`bootstrap 4`

![](https://img.shields.io/badge/author-Gaozih-%2366ccff)
![](https://img.shields.io/github/license/Gzh0821/WebBlog)
![](https://img.shields.io/github/stars/Gzh0821/WebBlog)


## 简介
- 这是一个由 Django, bootstrap和其它开源项目构建的简易博客系统。

- 该系统实现了基本的发表及修改文章，评论，用户管理，文章分类功能，同时集成了markdown语法。

- 使用简易的sqlite作为数据库。

- 代码易于复现和修改。

## 简易的安装与调试
### 配置python3和django环境
- **不建议使用本方法部署到实际生产服务器**

- **若您已安装python和django环境，可跳过本步骤**
- 安装`python 3.10`，可在[python.org](https://www.python.org)中下载
（windows平台安装时，请勾选：Add Python to environment variables）

- 部分系统预装有python2，执行以下命令时，请将`python`更改为`python3`
- （可选）使用`virtualenv`创建虚拟环境

### 配置项目设置
- 下载项目压缩包或使用git：`git clone https://github.com/Gzh0821/WebBlog.git` 命令，将项目文件下载到本地

- 在项目根目录下，您应该看到 `manage.py` 和 `requirements.txt` 文件，在此目录中打开终端/命令行窗口。

- 以下命令可能需要管理员/root权限

- 输入命令
- `pip3 install -r requirements.txt`安装项目需要的库

- 在终端中打开`python`（3.10）版本，使用以下命令获得一个新的 __SECRET_KEY__ 
```python3
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
- 使用`exit()`退出`python`环境
- 复制该 __SECRET_KEY__ ，打开项目子目录`WeBblog`，打开`settings_example.py`文件

- 找到以下段落，将复制的 __SECRET_KEY__ 粘贴到空引号内。
```
# Add your own SECRET_KEY here
SECRET_KEY = '(粘贴到此处)'
```

- 若需要 **DEBUG** 环境 ,请将文件内的 
```
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
```
  更改为
```
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
```

- 修改完成后，保存文件并将其**重命名**为`settings.py`

- 返回项目根目录（`manage.py`所在目录），在终端中输入：
```
python manage.py migrate
```
生成项目数据库。若成功，项目根目录下应出现`db.sqlite3`文件。
### 创建超级管理员，启动服务
- 在终端中输入：
```
python manage.py createsuperuser
```
根据提示创建管理账户。

- 若仅在本机访问项目网站（使用`localhost`本地回环），在终端中输入：
```
python manage.py runserver 127.0.0.1:8000 --insecure
```
- 若需作为服务器，使其它主机访问，则在终端中输入：
```
python manage.py runserver 0.0.0.0:8000 --insecure
```
- 成功启动服务后，终端应出现类似提示：
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

- 打开浏览器，输入`127.0.0.1:8000` 访问项目网站。
- 若您部署在服务器上，则输入服务器的ip地址:8000访问。

- 关闭终端或使用`Ctrl+C`结束服务

## 网站管理
### 进入管理界面
- 登录管理账户后，点击右上角用户，进入后台管理界面。
### 修改用户权限
- 新创建的用户默认无发表文章和发表评论的权限

- 点击“认证和授权”栏下的“用户”，选择要修改权限的用户，在`PROFILE`栏下，修改其功能：

- `Author permission` 为发表文章权限

- `Comment permission` 为评论权限

- 修改后，可在网站主页右上角用户的“个人信息”处查看权限
### 创建分类栏目
- 点击“ARTICLE”栏下的“栏目”，点击右上角“增加 栏目”

- 在`Title`栏输入栏目名称，保存即可

- 可添加多个栏目

- 修改后，在修改文章/创建文章界面，可选择文章所属的栏目。

