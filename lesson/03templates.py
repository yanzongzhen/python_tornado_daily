import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

define('port',default=8000,help='run port',type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('01index.html')

    def post(self):
        username = self.get_argument('name','no')
        passwd = self.get_argument('password','no')
        self.render('02tmep_index.html',username=username)

class TempHandler(tornado.web.RequestHandler):
    def haha(self):
        return '这里是tornado'

    def get(self):
        username = self.get_argument('name','no')
        import time
        li = ['a','b','c','d']
        self.render('02tmep_index.html',
                    username=username,
                    time=time,
                    haha=self.haha,
                    li=li
                    )


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/index',IndexHandler),
            (r'/temp',TempHandler),
        ],
        template_path='templates',
        static_path='static',
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()