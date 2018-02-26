import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

define('port',default=8000,help='run port',type=int)


class TestIndexHandler(tornado.web.RequestHandler):
    def get(self):
        abc = self.get_argument('abc','no')
        self.write('hello '+abc+'\n')
        # abc = self.get_arguments('abc')
        # self.write(','.j· oin(abc))
        print(abc)

class UserHandler(tornado.web.RequestHandler):
    def get(self,name,age):
        self.write('---name=%s---age=%s'%(name,age))

class BookNameHandler(tornado.web.RequestHandler):
    def get(self, name, age):
        '''通过url传入参数名是固定的'''
        print(self.request.remote_ip)
        self.write('-----name=%s --------age=%s-----%s------'%(name, age, self.request.remote_ip))

class WriteHandler(tornado.web.RequestHandler):
    def get(self):
        user = {
            'name':'budong',
            'age':18,
        }
        self.write(user)
        li = [1,2,3,4,'5']
        import json
        li = json.dumps(li)
        self.write(li)
        print(repr(li),type(li))
        li = json.loads(li)
        print(repr(li),type(li))

class HtmlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')  #html 的文件名

    def post(self):
        name = self.get_argument('name','no')
        passwd = self.get_argument('password','no')
        st = '---name=%s---password=%s---'%(name,passwd)
        self.write(st)

class MyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(self.request.remote_ip)
        print(self.request.remote_ip)
        print(self.request.connection)
        print(self.request.full_url())
        print(self.request.request_time())

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[
            (r'/test',TestIndexHandler),
            (r'/user/(.+)/([1-9]+)',UserHandler),
            (r'/bookname/(?P<name>.+)/(?P<age>[1-9]+)', BookNameHandler),
            (r'/write',WriteHandler),
            (r'/html',HtmlHandler),
            (r'/request',MyHandler),
        ],
        template_path='templates',
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


