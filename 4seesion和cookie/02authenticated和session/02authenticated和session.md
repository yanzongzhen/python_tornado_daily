# authenticated和session

##### 1.登录检查

#####2.authenticated

##### 3.session

##### 4.跨站防伪造请求的防范



###1.登录检查

我们登录的时候需要验证，但是如果有很多地方需要验证，这个时候就会出现很多重复代码的情况，这个时候我们需要一个不改变函数运行，又能给函数加上验证过程方法，很明显，我们可以使用装饰器来达到这个功能，代码如下：

```python
def auth(fun):
    def wrapper(self,*args,**kwargs):
        id = self.get_secure_cookie('ID')
        if id:
            return fun(self,*args,**kwargs)
        else:
            self.redirect('/login')
    return wrapper

#定义好装饰器之后，就可以直接去修饰需要验证的方法  
class IndexHandler(BaseHandler):
    @auth
    def get(self):
        self.write('登录成功---index')  
```

使用装饰器可以很方便我们去做登录检查，可以节省出大量的代码，增加程序的可读性和程序整体的美观。



### 2.authenticated

虽然我们自己可以做这个登录检查，但是在tornado内部给我们提供了一个内置的装饰器`authenticated`这个可以帮我们自动的进行登录验证，`authenticated`可以省去我们自己重复造轮子的过程，但是在使用的时候需要注意几点：

```python
# Application中添加配置
login_url='/login',

# 重写 get_current_user 方法
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        current_user = self.get_secure_cookie('ID')
        if current_user:
            return current_user
        return None
# 装饰需要验证的方法      
@authenticated      
```



有些时候我们需要跳转到之前的页面怎么做呢？当我们使用`authenticated`的时候我们可以十分方便的做这件事情。我们观察跳转之后的url就可以发现，如果是使用`authenticated`装饰器装饰之后，而跳转到登录页面之后，在登录页面的url中，可以看到最后面会添加上一个next参数，这个就是我们刚才跳转的路由，通过这个参数，我们就可以很方便的跳转回之前的的路由，具体实现如下:

```python
class LoginHandler(BaseHandler):
    def get(self):
        nextname = self.get_argument('next','')
        self.render('10authenticated.html',nextname=nextname)
    def post(self):
        nextname = self.get_argument('next', '')
        username = self.get_argument('name','')
        username = User.by_name(username)
        passwd = self.get_argument('password', '')
        print(username)
        if username and username[0].password == passwd:
            self.set_secure_cookie('ID',username[0].username,max_age=100)
            self.redirect(nextname)
        else:
            self.render('10authenticated.html',nextname=nextname)
```

页面代码做如下的改变就行：

```html
<form method="post" action="/login?next={{nextname}}">
    <p>用户名<br><input type="text" name="name"></p>
    <p>密码<br><input type="text" name="password"></p>
    <input type="submit">
</form>
```

配合使用模板的传参，可以很方便的进行跳转。



### 3.session

cookie中不能存放存放用户的敏感信息，那么cookie里面就只能存放一些随机的字符串，但是如果这样的话，那么服务器端又怎样知道是那个用户呢？

我们可以建立一个会话来做这件事情，这个会话里面会存储随机字符串和可以唯一确定用户的信息。

由于tornado没有内置session模块，所以使用pycket这个模块中封装好的session模块来，要想使用首先要安装：

```python
pip install pyckey
pip install redis
```

安装好之后就可以使用了，使用很简单，注意一下几点：

```python
from pycket.session import SessionMixin

# 1.在Application添加 pycket 的配置
pycket={
  'engine': 'redis',
  'storage': {
    'host': 'localhost',
    'port': 6379,
    'db_sessions': 5,
    'db_notifications': 11,
    'max_connections': 2**31,
  },
  'cookies': {
    'expires_days': 30,
    'max_age': 100
  },
},

# 2.改 self.set_secure_cookie 为 self.session.set
# self.set_secure_cookie('ID',username[0].username,max_age=100)
self.session.set('user',username[0].username)

# 3.改 self.get_secure_cookie 为 self.session.get
# current_user = self.get_secure_cookie('ID')
current_user = self.session.get('user')
```

以上就可以使用`session`了，这个`session`的工作原理是如下：

 	1. 使用`set`方法，为输入的用户信息生成一串随机字符串
 	2. 将这个字符串和对应的用户信息做成键值对，放到`redis`数据库中
 	3. 将字符串处理之后放入到`cookie`中，发送给浏览器
 	4. 浏览器请求时将`cookie`中的信息发送到服务器，`tornado`接受到之后解析出来，去`redis`查找，找到就验证成功

使用`session`有如下好处：

 	1. 可以不要在`cookie`中存放敏感信息
 	2. 减少数据传输需要的时间
 	3. 减少加密解密的时间

`session`的使用很简单，但是安全性会有一个很大的提升，因此使用非常多，一定要掌握使用方法。



###4.跨站防伪造请求的防范

[跨站伪造请求(Cross-site request forgery)](https://en.wikipedia.org/wiki/Cross-site_request_forgery)， 简称为 `XSRF`，是个性化 Web 应用中常见的一个安全问题。前面的链接也详细讲述了` XSRF `攻击的实现方式。

当前防范` XSRF` 的一种通用的方法，是对每一个用户都记录一个无法预知的` cookie `数据，然后要求所有提交的请求中都必须带有这个` cookie `数据。如果此数据不匹配 ，那么这个请求就可能是被伪造的。

`Tornado `有内建的 `XSRF `的防范机制，要使用此机制，只需要在模板中添加如下代码：

```html
<form method="post" action="/login?next={{nextname}}">
    {% module xsrf_form_html() %}   <!--添加这行代码就可以了-->
    <p>用户名<br><input type="text" name="name"></p>
    <p>密码<br><input type="text" name="password"></p>
    <input type="submit">
</form>
```

