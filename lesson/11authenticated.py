import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
import util.uimodules
import util.uimethod
from tornado.web import authenticated
from pycket.session import SessionMixin

from data.user_modules import User,session

define('port', default=8000, help='run port', type=int)


def auth(fun):
    def wrapper(self, *args, **kwargs):
        id = self.get_secure_cookie('ID')
        if id:
            return fun(self,*args,**kwargs)
        else:
            self.redirect('/login')
    return wrapper


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
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
        # id = self.get_secure_cookie('ID')
        # if id:
        #     self.write('登录成功---index')
        # else:
        #     self.redirect('/login')
        self.write('登录成功---index')



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


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/index', IndexHandler),
            (r'/login', LoginHandler),
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
                'expires_days': 30,
                'max_age': 100
            },
        },
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()