import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

define('port',default=8000,help='run port',type=int)
# define('version',default='0.0.1',help='version 0.0.1',type=str)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('abc')

class AbcIndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('budong')

class TestIndexHandler(tornado.web.RequestHandler):
    def get(self):
        abc = self.get_argument('abc','no')
        self.write('hello '+abc)
        # abc = self.get_arguments('abc')
        # self.write(','.j· oin(abc))
        print(abc)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    # print(options.port)
    # print(options.version)
    app = tornado.web.Application(
        handlers=[
            (r'/',IndexHandler),
            (r'/abc',AbcIndexHandler),
            (r'/test',TestIndexHandler),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


