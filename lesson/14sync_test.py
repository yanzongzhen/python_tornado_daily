import time
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define,options
from tornado.web import authenticated
from pycket.session import SessionMixin
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import requests

define('port', default=8010, help='run port', type=int)


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None


class AbcHandler(BaseHandler):
    def get(self):
        self.write('OK')

# abc 和 sync 是同步的
class SyncHanler(BaseHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()  # 同步方法
        response = client.fetch('http://127.0.0.1:8000/sync?id=2') # 阻塞 调用
        print(response)
        self.write(response.body)


# tornado 是单线程的
class CallbackHandler(BaseHandler):
    """通过回调函数来实现异步"""
    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()   # 异步的方法
        client.fetch("http://127.0.0.1:8000/sync?id=2",callback=self.on_response)
        self.write('Ok!'+'<br>')

    def on_response(self,response):
        print(response)
        self.write(response.body)
        self.finish()   # 必须要加上


class GenHandler(BaseHandler):
    """通过协程实现的异步"""
    @tornado.web.asynchronous
    @tornado.gen.coroutine   # coroutine 协程
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,"http://127.0.0.1:8000/sync?id=3")
        print(response)
        self.write(response.body)


class FuncHandler(BaseHandler):
    """通过协程实现的异步"""
    @tornado.web.asynchronous
    @tornado.gen.coroutine   # coroutine 协程
    def get(self):
        response = yield self.func()
        print(response)
        self.write(response.body)

    @tornado.gen.coroutine
    def func(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,"http://127.0.0.1:8000/sync?id=4")
        raise tornado.gen.Return(response)


class MyFuncHandler(BaseHandler):
    """通过协程实现的异步"""
    executor = ThreadPoolExecutor()
    @tornado.web.asynchronous
    @tornado.gen.coroutine   # coroutine 协程
    def get(self):
        response = yield self.func()
        print(response)
        self.write(response.text)

    @run_on_executor
    def func(self):
        response = requests.get("http://127.0.0.1:8000/sync?id=4")
        return response



if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/abc', AbcHandler),
            (r'/sync', SyncHanler),
            (r'/callback', CallbackHandler),
            (r'/gen', GenHandler),
            (r'/func', FuncHandler),
            (r'/myfunc', MyFuncHandler),
        ],
        template_path='templates',
        static_path='static',
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()