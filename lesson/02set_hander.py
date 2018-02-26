import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

define('port',default=8000,help='run port',type=int)


class FlushHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('this is '+'<br>')
        self.write('tornado'+'<br>')
        self.flush()
        import time
        time.sleep(5)
        self.write('hahaha'+'<br>')
        # self.finish()
        # self.write('en~~~~')
        # self.send_error(404)
        # self.set_status(404,'error')

    def write_error(self, status_code, **kwargs):
        self.write("---%d----\n"%status_code)

class HeadersHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('headers')

        self.set_header('budong','18')
        self.set_header('changsha','hunan')

        self.set_header('budong','20')
        self.add_header('budong','19')
        self.add_header('changsha','0731')

        self.clear_header('changsha')



if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/flush',FlushHandler),
            (r'/header',HeadersHandler),
        ],
        template_path='templates',
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()