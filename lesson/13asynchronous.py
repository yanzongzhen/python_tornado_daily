import time
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define,options
import util.uimodules
import util.uimethod
from tornado.web import authenticated
from pycket.session import SessionMixin

from data.user_modules import User,session

define('port', default=8000, help='run port', type=int)

# 长轮询  long poll
# websocket

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None


class IndexHandler(BaseHandler):
    # @auth
    @authenticated
    def get(self):
        self.render('11websocket.html')

class MessageWSHandler(BaseWebSocketHandler):
    users = set()

    def open(self):
        MessageWSHandler.users.add(self)  # 有新的 WebSocket链接时调用这个函数
        print('-------------------------open------------------')

    def on_message(self, message):
        print(self.request.remote_ip)
        print(self.users)
        print(message,self.current_user)
        for u in self.users:
            # write_message tornado提供，主动给客户端发送消息
            u.write_message('%s-%s-说：%s'%(
                self.current_user,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                message
                ))


    def on_close(self):
        print('----------------on_close---------------')
        if self in MessageWSHandler.users:
            MessageWSHandler.users.remove(self)
        print(MessageWSHandler.users)


class LoginHandler(BaseHandler):
    def get(self):

        nextname = self.get_argument('next', '')
        self.render('10authenticated.html', nextname=nextname)

    def post(self):
        nextname = self.get_argument('next', '')
        username = self.get_argument('name', '')
        username = User.by_name(username)
        passwd = self.get_argument('password', '')
        print(username)
        if username and username[0].password == passwd:
            # self.set_secure_cookie('ID',username[0].username,max_age=100)
            self.session.set('user',username[0].username)
            self.redirect(nextname)
        else:
            self.render('10authenticated.html',nextname=nextname)


class SyncHanler(BaseHandler):
    def get(self):
        id = self.get_argument('id',1)
        user1 = User.by_id(id)
        time.sleep(10)
        user = {
            'username': user1[0].username,
            'userid': user1[0].id
        }
        self.write(user)



if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/index', IndexHandler),
            (r'/login', LoginHandler),
            (r'/websocket', MessageWSHandler),
            (r'/sync', SyncHanler),
        ],
        template_path='templates',
        static_path='static',
        ui_methods=util.uimethod,
        ui_modules=util.uimodules,
        cookie_secret='afjioasdhvawurigneuirghashvzshv',
        login_url='/login',
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
                'expires_days': 1,
                'max_age': 60*60
            },
        },
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()