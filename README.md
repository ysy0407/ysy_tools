### 一、简介
这里包含了我开发的一些python的脚本，用于帮助我的女朋友和朋友解决一些日常问题\
为避免大家都在本地需要安装python环境，在本地运行时出现问题，故开发了此简单的页面以供使用\
嗯...丑是正常的\
BaLaBaLa...
### 二、特点
* 通过sqlite数据库简单配置，即可实现网页传入文本、文件运行python脚本
* 实现简单的用户可使用工具控制、工具使用次数统计
### 三、技术栈
* python
* uwsgi
* flask
* sqlite3
### 四、消耗很多查克拉的工具
* handle_wx_covid19_test_picture：通过优化基于UIAutomation的wxauto，实现了自动滚动屏幕将微信中聊天的图片进行保存，且命名为昵称+群昵称。可以帮助居委会进行抗原、核酸的图片的收集和统计啦
* echocardiography_data_handle：处理超声数据文件，帮女朋友写的，后来她朋友也用了，虽然简单但好评满满^_^
* oxford_paper_download：帮发小整的自动下载文章，类似爬虫？包含了html解析，标签查找什么的
* ......（其实没啥了）
#### 需手动安装的依赖
pip install uwsgi\
pip install flask\
pip install flask_login\
pip install python-docx\
pip install openpyxl\
没写完