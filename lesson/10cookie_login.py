import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

import util.uimodules
import util.uimethod

from data.user_modules import User,session

define('port',default=8000,help='run port',type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_secure_cookie('ID')
        if id:
            self.write('登录成功---index')
        else:
            self.redirect('/login')


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('09login.html')
    def post(self):
        username = self.get_argument('name','')
        username = User.by_name(username)
        passwd = self.get_argument('password', '')
        print(username)
        if username and username[0].password == passwd:
            self.set_secure_cookie('ID',username[0].username,max_age=100)
            self.write('登录成功---post')
            time.sleep(3)
            self.redirect('/index')
        else:
            self.render('09login.html')




if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/index',IndexHandler),
            (r'/login',LoginHandler),
        ],
        template_path='templates',
        static_path='static',
        ui_methods=util.uimethod,
        ui_modules=util.uimodules,
        cookie_secret='afjioasdhvawurigneuirghashvzshv',
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()