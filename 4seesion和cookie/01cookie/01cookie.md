# cookie

##### 1.cookie的了解

##### 2.cookie的设置



###1.cookie的了解

cookie是网站为了辨别用户身份而储存在用户本地终端（Client Side）上的数据（通常经过加密）。

**分类**

Cookie总是保存在客户端中，按在客户端中的存储位置，可分为内存Cookie和硬盘Cookie。内存Cookie由浏览器维护，保存在内存中，浏览器关闭后就消失了，其存在时间是短暂的。硬盘Cookie保存在硬盘里，有一个过期时间，除非用户手工清理或到了过期时间，硬盘Cookie不会被删除，其存在时间是长期的。所以，按存在时间，可分为非持久Cookie和持久Cookie。

**用途**

因为HTTP协议是无状态的，即服务器不知道用户上一次做了什么，这严重阻碍了交互式Web应用程序的实现。在典型的网上购物场景中，用户浏览了几个页面，买了一盒饼干和两瓶饮料。最后结帐时，由于HTTP的无状态性，不通过额外的手段，服务器并不知道用户到底买了什么。 所以Cookie就是用来绕开HTTP的无状态性的“额外手段”之一。服务器可以设置或读取Cookies中包含信息，借此维护用户跟服务器会话中的状态。

在刚才的购物场景中，当用户选购了第一项商品，服务器在向用户发送网页的同时，还发送了一段Cookie，记录着那项商品的信息。当用户访问另一个页面，浏览器会把Cookie发送给服务器，于是服务器知道他之前选购了什么。用户继续选购饮料，服务器就在原来那段Cookie里追加新的商品信息。结帐时，服务器读取发送来的Cookie就行了。

Cookie另一个典型的应用是当登录一个网站时，网站往往会请求用户输入用户名和密码，并且用户可以勾选“下次自动登录”。如果勾选了，那么下次访问同一网站时，用户会发现没输入用户名和密码就已经登录了。这正是因为前一次登录时，服务器发送了包含登录凭据（用户名加密码的某种加密形式）的Cookie到用户的硬盘上。第二次登录时，（如果该Cookie尚未到期）浏览器会发送该Cookie，服务器验证凭据，于是不必输入用户名和密码就让用户登录了。

**缺陷**

1. Cookie会被附加在每个HTTP请求中，所以无形中增加了流量。
2. 由于在HTTP请求中的Cookie是明文传递的，所以安全性成问题。
3. Cookie的大小限制在4KB左右。对于复杂的存储需求来说是不够用的。

以上信息来自[维基百科](https://zh.wikipedia.org/wiki/Cookie)



###2.cookie的设置

在`Tornado`中，cookie是默认不设置的，如果需要的的话，需要自己去设置，设置很简单，使用提供的`set_cookie`方法就可以设置一个`cookie`

```python
class CookieHandler(tornado.web.RequestHandler):
    def get(self):
        import time
        # self.set_cookie('cookie_test','this_is_test')
        # self.set_cookie('cookie_test','this_is_test',expires=time.time()+60) #如果没有则是默认浏览器结束时过期 过期时间是60秒
        # self.set_cookie('cookie_test','this_is_test',expires_days=1)# 过期时间一天
        # self.set_cookie('cookie_test','this_is_test',path='/')# 设置匹配路径  这是所有的路由都可以获取
        # self.set_cookie('cookie_test','this_is_test',httponly=True)# 设置True js不可获取cookie
        # self.set_cookie('cookie_test','this_is_test',expires=time.time()+60 ,max_age=120)# max_agede 优先级要高
        self.set_secure_cookie('secure_cookie','secure')
        se = self.get_cookie('secure_cookie')
        print(se)
        se = self.get_secure_cookie('secure_cookie')
        print(se)
        # self.clear_cookie('secure_cookie')
        self.clear_all_cookies()
        self.write('cookie test')
```







