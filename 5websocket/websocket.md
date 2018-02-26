# WebSocket

##### 1.长轮询与websocket介绍

##### 2.websocket编程



### 1.长轮询与websocket介绍

**长轮询**

长久以来, 创建实现客户端和用户端之间双工通讯的`web app`都会造成`HTTP`轮询的滥用: 

​	客户端向主机不断发送不同的`HTTP`呼叫来进行询问。

这会导致一系列的问题：

1. 服务器被迫为每个客户端使用许多不同的底层`TCP`连接：一个用于向客户端发送信息，其它用于接收每个传入消息。
2. 有线协议有很高的开销，每一个客户端和服务器之间都有`HTTP`头。
3. 客户端脚本被迫维护从传出连接到传入连接的映射来追踪回复。

一个更简单的解决方案是使用单个`TCP`连接双向通信。 这就是`WebSocket`协议所提供的功能。 结合`WebSocket API` ，`WebSocket`协议提供了一个用来替代`HTTP`轮询实现网页到远程主机的双向通信的方法。

**webscoket介绍**

`WebSocket`协议是基于`TCP`的一种新的网络协议。它实现了浏览器与服务器全双工`(full-duplex)`通信——允许服务器主动发送信息给客户端。`WebSocket`通信协议于2011年被`IETF`定为标准`RFC 6455`，并被`RFC7936`所补充规范。

在实现`websocket`连线过程中，需要通过浏览器发出`websocket`连线请求，然后服务器发出回应，这个过程通常称为“握手” 。在 `WebSocket API`，浏览器和服务器只需要做一个握手的动作，然后，浏览器和服务器之间就形成了一条快速通道。两者之间就直接可以数据互相传送。在此`WebSocket `协议中，为我们实现即时服务带来了两大好处：

1.  `Header`互相沟通的`Header`是很小的,大概只有 `2 Bytes`
2.  `Server Push`服务器的推送，服务器不再被动的接收到浏览器的请求之后才返回数据，而是在有新数据时就主动推送给浏览器。

**websocket的建立过程**

浏览器请求：

```python
GET /webfin/websocket/ HTTP/1.1		# HTTP请求方式
Host: localhost					   # 
Origin: http://服务器地址		    #
Cookie:_aaa						   # cookie
#以下是建立webscoket链路的核心。  
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Key: xqBt3ImNzJbYqRINxEFlkg==   # 密钥
Sec-WebSocket-Version: 13            # websocket版本
```

服务器回应

```python
HTTP/1.1 101 Switching Protocols
...

Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: K7D JLdLooIwIG/MOpvWFB3y3FE8=

WebSocket借用http请求进行握手，相比正常的http请求，多了一些内容。其中:
	Upgrade: websocket
	Connection: Upgrade
表示希望将http协议升级到Websocket协议。

Sec-WebSocket-Key是浏览器随机生成的base64 encode的值，用来询问服务器是否是支持WebSocket。
服务器返回:
	Upgrade: websocket
	Connection: Upgrade

告诉浏览器即将升级的是Websocket协议.
Sec-WebSocket-Accept是将请求包“Sec-WebSocket-Key”的值，与”258EAFA5-E914-47DA-95CA-C5AB0DC85B11″这个字符串进行拼接，然后对拼接后的字符串进行sha-1运算，再进行base64编码得到的。用来说明自己是WebSocket助理服务器。

Sec-WebSocket-Version是WebSocket协议版本号。RFC6455要求使用的版本是13，之前草案的版本均应当被弃用。 
更多握手规范详见RFC6455。
```



###2. websocket编程

websocket的编程分为服务端编程和客户端编程。

**服务端编程**

Tornado定义了 tornado.websocket.WebSocketHandler 类用于处理 WebSocket 链接的请求，应用开发者应该继承该类并实现其中的open()、on_message()、on_close() 函数。

除了这3个 Tornado 框架自动调用的入口函数，WebSocketHandler 还提供了两个开发者主动操作 WebSocket的函数。

* WebSocketHandler.write_message(message)函数：用于向与本链接相对应的客户端写消息
* WebSocketHandler.close(code=None,reason=None)函数：主动关闭 WebSocket链接。其中的code和reason用于告诉客户端链接被关闭的原因。参数code必须是一个数值，而reason是一个字符串。

```python
class BaseWebSocketHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None

class MessageWSHandler(BaseWebSocketHandler):
    users = set()

    def open(self):
        # 有新的websocket链接时调用这个函数
        MessageWSHandler.users.add(self)
        print('-------------------open-----------------')

    def on_message(self, message):
        print(message,self.current_user)
        for u in self.users:
            u.write_message('%s-%s-说:%s'%(self.current_user.username,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),message))

    def on_close(self):
        print('-------------------on_close-----------------')
        # 当websocket链接关闭时调用这个函数
        if self in MessageWSHandler.users:
            MessageWSHandler.users.remove(self)
        print(MessageWSHandler.users)
```



**客户端编程**

由于 WebSocket 是 HTML5 的标准之一，所以主流浏览器的 web 客户端编程语言 Javascript 已经支持 WebSocket 的客户端编程。

客户短编程围绕着 WebSocket 对象展开，在 Javascript  中可以通过如下代码初始化 WebSocket 对象：

```js
var socket = new WebSocket(url ):
```

在代码中只需给 WebSocket构造函数传入服务器的URL地址，可以为该对象的如下事件指定处理函数以响应它们。

* WebSocket.onopen ：此事件发生在 WebSocket 链接建立时
* WebSocket.onmessage ：此事件发生在收到了来自服务器的消息时
* WebSocket.onclose ：此事件发生在与服务器的链接关闭时
* WebSocket.onerror ：此事件发生在通信过程中有任何错误时

除了这些事件处理函数，还可以通过 WebSocket 对象的两个方法进行主动操作

* WebSocket.send(data) ：向服务器发送消息
* WebSocket.close() ：主动关闭现有链接

参考代码如下：

```html
<body>
  
    <div>
        <textarea id="text"></textarea>
        <a href="javascript:WebSocketTest();">发送</a>
    </div>
    <div id="messages" style="height:500px;overflow: auto;"></div>
  
 	<script src="{{static_url('js/jquery-2.2.0.min.js')}}"></script>
 	<!--<script src="{{static_url('js/bootstrap.min.js')}}"></script>-->
  
    <script type="text/javascript">
        var mes = document.getElementById('messages');
        function WebSocketTest() {
            if("WebSocket" in window){
                mes.innerHTML = "发送Websocket请求成功!";
                var ws = new WebSocket("ws://127.0.0.1:8000/websocket");
                ws.onopen = function () {
                    ws.send($("#text").val()) ;
                };
                ws.onmessage = function (evt) {
                    var received_msg = evt.data;
                    mes.innerHTML = mes.innerHTML +
                            "<br>服务器已收到信息：<br>" + received_msg;
                };
                ws.onclose = function () {
                  mes.innerHTML = mes.innerHTML + "<br>连接已经关闭...";
                };
            } else {
                mes.innerHTML = "发送Websocket请求失败!";
            }
        }
    </script>
</body>
```









