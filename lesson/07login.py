import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

import util.uimodules
import util.uimethod

from data.user_modules import User,session

define('port',default=8000,help='run port',type=int)

class AuthError(Exception):
    def __init__(self,msg):
        super(AuthError,self).__init__(msg)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = 'no'
        self.render('08sqlalchemy.html',username=username)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('08login.html',error=None)
    def post(self):
        username = self.get_argument('name','')
        username = User.by_name(username)
        passwd = self.get_argument('password','')
        if username and username[0].password == passwd:
            self.render('08sqlalchemy.html',
                        username=username[0].username
                        )
        else:
            self.render('08login.html',error='登陆失败')

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('08register.html',error=None)

    def post(self):
        if self._check_argument():
            try:
                self._create_user()
                self.render('08login.html',error=None)
            except AuthError as e:
                self.render('08register.html',error=e)
            except Exception as e:
                self.render('08register.html',error=e)
        else:
            self.render('08register.html',error='input error')

    def _check_argument(self):
        username = self.get_argument('name','')
        passwd = self.get_argument('password1','')
        if len(username)<10 and len(passwd)<10:
            return True
        else:
            return False

    def _create_user(self):
        if User.by_name(self.get_argument('name','')):
            raise AuthError('Name is registered')
        if self.get_argument('password1','') != self.get_argument('password2',''):
            raise AuthError('Password error')
        user = User()
        user.username = self.get_argument('name','')
        user.password = self.get_argument('password1','')
        session.add(user)
        session.commit()


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/',IndexHandler),
            (r'/login',LoginHandler),
            (r'/register',RegisterHandler),
        ],
        template_path='templates',
        static_path='static',
        ui_methods=util.uimethod,
        ui_modules=util.uimodules,
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()