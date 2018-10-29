# 简易图书馆管理系统
## 前言
这个是2018大四上学期写的一个软件工程课程设计，主要涉及了Django和Sqlite3,和少量bootstrap,参考的学习资料有[Django官方文档](https://docs.djangoproject.com/zh-hans/2.1/),[bootstrap官方文档](https://getbootstrap.com/),以及B站up主[捷佳](https://space.bilibili.com/179328791/#/)的视频，做的特别好，推荐入门Django观看
## 实验课题
学校图书馆图书管理系统：
 1. 用于学校图书馆对图书进行管理，例如图书入库、图书借还等等，借书人员仅限于学校老师和学生，老师最多借8本书，学生最多可以借6本书，一本书的借书时间不得 超过60天。
 2. 读者可以通过系统查看图书馆库存、自己的借阅历史等，可以通过系统预约借书，每人最多预约3本书
 3. 读者可以对所读图书进行评论
 
## 运行环境
在python3.6.6,Django2.1版本下测试运行成功，linux平台。其余情况未测试
## 运行步骤
首先安装好运行环境，配置好python虚拟环境，可以不使用虚拟环境,进入LmsWeb目录
```
python manage.py makemigrations
python manage.py migrate
上面两步进行迁移，完成数据库表的建立
python manage.py runserver
默认端口开在127.0.0.1:8000
```
然后浏览器打开127.0.0.1:8000/lms进入管理系统，127.0.0.1:8000/admin进入后台管理
## 结语
Django学习过程中写的一个简易的小项目，希望能给大家的学习带来点帮助
