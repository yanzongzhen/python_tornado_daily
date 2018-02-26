import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

define('port',default=8000,help='run port',type=int)



class TempHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('name','no')
        urllist = [
            ('https://www.shiguangkey.com','时光课堂'),
            ('https://www.baidu.com','百度'),
            ('https://www.zhihu.com','知乎'),
        ]
        atga = "<a href='https://www.baidu.com' target='_blank'>___百度___</a><br>" #转义
        self.render('03escape.html',
                    username=username,
                    urllist=urllist,
                    atga=atga
                    )


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/temp',TempHandler),
        ],
        template_path='templates',
        static_path='static',
        # autoescape=None,  #全局
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()