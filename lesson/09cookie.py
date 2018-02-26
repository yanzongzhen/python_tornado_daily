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
        # self.set_cookie('cookie_test','this_is_test')  #默认过期时间是关闭浏览器
        # self.set_cookie('cookie_test','this_is_test',expires=time.time()+60) #设置的是60秒
        # self.set_cookie('cookie_test','this_is_test',expires_days=1) #设置的是一天
        # self.set_cookie('cookie_test','this_is_test',path='/') #设置路径
        # self.set_cookie('cookie_test','this_is_test',httponly=True) #设置js不可以后去cookie
        # self.set_cookie('cookie_test','this_is_test',max_age=120,expires=time.time()+60) #max_age优先级高
        # self.set_secure_cookie('cookie_test','this_is_test') #
        self.clear_cookie('cookie_test')
        self.clear_all_cookies()
        self.write('cookie test')


class GetCookieHandler(tornado.web.RequestHandler):
    def get(self):
        co = self.get_cookie('cookie_test')
        self.write(co)
        self.write('<br>')
        co = self.get_secure_cookie('cookie_test')
        self.write(co)



if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/index',IndexHandler),
            (r'/getcookie',GetCookieHandler),
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