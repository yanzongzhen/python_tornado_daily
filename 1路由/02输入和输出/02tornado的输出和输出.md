# Tornado的输入和输出

##### 1.输入函数

##### 2.输出函数



### 1.输入函数

```python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

define('port',default=8000,help='run port',type=int)

class TestIndexHandler(tornado.web.RequestHandler):
    def get(self):
        abc = self.get_argument('abc','no')
        # self.write('hello '+abc)
        abc = self.get_arguments('abc')
        self.write(','.join(abc))
        print(abc)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # print(options.port)
    # print(options.version)
    app = tornado.web.Application(
        handlers=[
            (r'/test',TestIndexHandler),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
```

在上节课我们简单介绍了`get_argument`和`get_arguments`的区别和用法，今天详细介绍一下这两个方法。



 [`get_argument` ](http://www.tornadoweb.org/en/stable/_modules/tornado/web.html#RequestHandler.get_argument)函数获取查询字符串或者请求体中的信息

​	查询字符串：就是在浏览器的地址栏看到的url中“？”后面的字符串

​	请求体：在POST请求中的body数据，比如表单数据form data、json数据、xml数据

函数原型：（返回具有给定名称的参数的值。返回的值始终是unicode）

`RequestHandler.get_argument（*name*，*default = *，*strip = True *）`

```
参数说明：
- 如果未提供default 值，则认为该参数是必需的，如果缺少该参数则抛出 MissingArgumentError异常。
- 如果参数多次出现在url中，我们返回最后一个值。
- strip = True，默认为剪切字符串两边的空格
```

通过[`get_arguments` ](http://www.tornadoweb.org/en/stable/_modules/tornado/web.html#RequestHandler.get_arguments)函数获取查询字符串或者请求体中的信息

函数原型：返回具有给定名称的参数的值的列表。返回的值始终是unicode，如果参数不存在返回空列表

`RequestHandler.get_arguments`（*name*，*strip = True *）

除此之外，还有：

```python
RequestHandler.get_query_argument（name，default = <object object>，strip = True ）
RequestHandler.get_query_arguments（name，strip = True ）
RequestHandler.get_body_argument（name，default = <object object>，strip = True ）
RequestHandler.get_body_arguments（name，strip = True ）
```

在之前我们都是使用url来获取字符串，通过URI来获取参数的时候有两种风格

```python
#查询字符串风格
http://127.0.0.1:8000/test?abc=不动

#符合REST风格的url
http://127.0.0.1:8000/user/不动/18
```

当时使用REST风格的写法时，路由映射的写法：

```python
(r'/user/(.+)/([1-9]+)',UserHandler), #通过url名称不固定的传参
(r'/bookname/(?P<name>.+)/(?P<age>[1-9]+)', BookNameHandler),#通过url传固定名称的参数,名字固定为name age
```

Handler的写法

```python
class UserHandler(tornado.web.RequestHandler):
    def get(self,name,age):
        self.write('---name=%s---age=%s'%(name,age))

class BookNameHandler(tornado.web.RequestHandler):
    def get(self, name, age):
        '''通过url传入参数名是固定的'''
        print(self.request.remote_ip)
        self.write('-----name=%s --------age=%s-----%s------'%(name, age, self.request.remote_ip))     #self.request.remote_ip 得到请求主机的IP
```





#### 2.输出函数

函数原型:

[`RequestHandler.write(*chunk*)`](http://www.tornadoweb.org/en/stable/_modules/tornado/web.html#RequestHandler.write)

- 将给定的块写入输出缓冲区。

- 要将输出写入网络，请使用下面的flush（）方法

- 如果给定的块是字典，我们将其写为JSON，并将响应的Content-Type设置为application/json。（如果要发送JSON作为其他的Content-Type，调用write（）后调用set_header ）。

- 请注意，由于潜在的跨站点安全漏洞，列表不会转换为JSON。所有JSON输出都应该包装在字典中。

  ```python
  (r'/write',WriteHandler),

  class WriteHandler(tornado.web.RequestHandler):
      def get(self):
          user = {
              'name':'budong',
              'age':18,
          }
          self.write(user)  #wirte 回去的就是字符串
          
          li = [1,2,3,4]
          import json
          li = json.dumps(li)
          self.write(li)
          print(repr(li),type(li))
          li = json.loads(li)
          print(repr(li),type(li))        
  ```

  ​

函数原型：

[`RequestHandler.render（*template_name*，**\* kwargs *）`](http://www.tornadoweb.org/en/stable/_modules/tornado/web.html#RequestHandler.render)

返回html页面，页面中可以添加变量和函数。

```python
(r'/html',HtmlHandler),
template_path='templates',

class HtmlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')  #html 的文件名

#templates 必须在一个lesson下面，一个文件夹下面，它自己是从起服务这个地方开始找的
```

html页面如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test</title>
</head>
<body>
hello budong
</body>
</html>
```



上面这些就是tornado的输入和输出，从前台获取数据，就是输入，后台把数据返回给前台，就是输出。

接下来我们看看如果是post请求，改怎么得到信息：

首先在之前的html中添加下面内容：

```html
<form method="post" action="/html">
    <p>用户名<br><input type="text" name="name"></p>
    <p>密码<br><input type="text" name="password"></p>
    <input type="submit">
</form>
```

在HtmlHandler中添加如下代码：

```python
def post(self):
    name = self.get_argument('name','no')
    passwd = self.get_argument('password','no')
    st = '---name=%s---password=%s---'%(name,passwd)
    self.write(st)
```

get和post的区别是:get就是获取服务器数据的意思，post是类似于提交数据，往服务器提交数据。

接下来我们看看，我们可以从前台的请求中获取些什么信息：

```python
(r'/request',MyHandler),
class MyHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.remote_ip)
```

今天就这么些内容，大家整理一下输入和输出，怎样得到输入和输出。













