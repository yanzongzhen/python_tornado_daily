###self.request可以获取到的请求信息

| method          | HTTP请求方法，例如“GET”或“POST”                  |
| --------------- | ---------------------------------------- |
| uri             | 请求的完整uri                                 |
| path            | 路径部分的uri                                 |
| query           | 查询部分的uri                                 |
| version         | 请求中指定的HTTP版本，例如“HTTP / 1.1”              |
| headers         | [`HTTPHeaders`](http://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPHeaders)用于请求标题的类似字典的对象。request.headers["aaa"] 像一个不区分大小写的字典一样使用附加的重复标题的方法。 |
| body            | 请求主体（如果存在）作为字节串                          |
| remote_ip       | 客户端的IP地址作为字符串。如果`HTTPServer.xheaders`设置，将传递由负载均衡器在`X-Real-Ip`或`X-Forwarded-For`头中提供的真实IP地址。版本3.1更改：`X-Forwarded-For`现在支持列表格式。 |
| protocol        | 所使用的协议是“http”或“https”。如果`HTTPServer.xheaders` 设置，将通过负载均衡器使用的协议（如果通过`X-Scheme`头部报告）传递。 |
| host            | 请求的主机名，通常取自`Host`标题                      |
| arguments       | 参数属性中提供GET / POST参数，它将参数名称映射到值列表（以支持单个名称的多个值）。名称是类型[`str`](https://docs.python.org/3.5/library/stdtypes.html#str)，而参数是字节字符串。请注意，这不同于 [`RequestHandler.get_argument`](http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.get_argument)，它将参数值作为unicode字符串返回。 |
| query_arguments | 与`arguments`格式相同 但只包含从查询字符串中提取的参数。版本3.2中的新功能 |
| body_arguments  | 与`arguments`格式相同 但只包含从请求体提取的参数。版本3.2中的新功能。 |
| files           | 文件属性中可以使用文件上传，它将文件名映射到列表`HTTPFile`。 `tornado.httputil.``HTTPFile`表示通过表单上传的文件。为了向后兼容，其实例属性也可作为字典键访问。 |
| full_url()      | 重新构建此请求的完整URL。                           |
| request_time()  | 返回此请求执行所花费的时间。                           |

