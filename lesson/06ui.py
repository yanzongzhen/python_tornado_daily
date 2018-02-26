import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

import util.uimodules
import util.uimethod

define('port',default=8000,help='run port',type=int)

class Calculation:
    def sum(self,a,b):
        return a+b

class UiHandler(tornado.web.RequestHandler):
    def fun(self):
        return 'zhangxiong'

    def get(self):
        username = self.get_argument('name','no')
        self.render('07module.html',
                    username=username,
                    fun=self.fun,
                    cal=Calculation
                    )


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/ui',UiHandler),
        ],
        template_path='templates',
        static_path='static',
        ui_methods=util.uimethod,
        ui_modules=util.uimodules,
        # ui_modules={'UiModule':util.uimodules.UiModule},
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()