# Tornado的ui_modules和ui_methods

##### 1.模板中导入方法和类

##### 2.ui_modules和ui_methods

### 1.模板中导入方法和类

在之前我们讲过了在模板中传入函数的方法，我们先来回顾一下

```python
class UiIndexHandler(tornado.web.RequestHandler):
    def fun(self):
        return "this is funcation"

    def get(self):
        username = self.get_argument('name','no')
        self.render('07module.html',username=username,fun=self.fun)
```

页面如下

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Module</title>
</head>
<body>
登录用户是{{ username }}
<br>
{{ fun() }}
<br>
</body>
</html>
```

这是之前讲过的内容，除此之外类也是可以传入的

```python
class Calculation:
    def sum(self,a,b):
        return a+b
```

在页面中调用

```html
{{ cal() }}   <!--实例化-->
<br>
{{ cal().sum(6,9) }}
```

除了上面这些语法之外，我们还可以直接在HTML文件中导入方法或者类

导入模块

```python
{% import module %}
```

导入指定模块

```python
{% from x import y %}
```

例子

```html
{% import time %}
{{ time.time() }}
```

在模板中也可以直接导入自定义的类或方法

```python
{% from util.mode_file import sub,upper,Count %}
```

实例如下

```html
{{ sub(5,3)}}
<br>
{{ Count().url() }}
<br>
{% raw Count().url() %}<br>
{{ Count.sum(7,1) }}<br>
{{ Count().sum(7,1) }}<br>
```

我们发现上面的这些方式都是写在类里面或者模块里面，复用性不强，如果要复用，可以使用一下的方式。

###2.ui_modules和ui_methods

第一步：新建文件uimethods.py ，这里的文件名是随意的只要在import时合法就行

```python
def methods1(self):  #注意这里要加上self
    return  'ui_methods 1'

def methods2(self):
    return  'ui_methods 2'
```

新建文件uimodules.py，使用ui_modules需要继承UIModule类

```python
from tornado.web import UIModule
class UiModule(UIModule):
    def render(self, *args, **kwargs):
        return '我是ui_module'
```

第二步：在项目中导入

```python
import util.uimethods
import util.uimodules
```

第三步：在application配置参数，值是导入的模块名

```python
ui_methods=util.uimethods,
ui_modules=util.uimodules,
#也可以写成字典的形式，其实在tornado内部就是解析成字典的形式
ui_modules={'UiModule':util.uimodules.UiModule},
```

第四步：在HTML中调用，导入的ui_modules需要使用module语句调用

```html
<!--调用ui_modules-->
{% module UiModule() %}<br>
<br>
<!--调用ui_methodes-->
{{ methods1() }}
```

ui_modules和ui_methods提高了方法和类的复用性，可以在全局使用。

开看看下面这个例子，我们页面上弹出一个小的弹窗

uimodules.py添加如下代码

```python
class Advertisement(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('07ad.html')

    def css_files(self):
        return "/static/css/King_Chance_Layer7.css"

    def javascript_files(self):
        return [
            "/static/js/jquery_1_7.js",
            "/static/js/King_Chance_Layer.js",
            "/static/js/King_layer_test.js"
        ]
```

增加07ad.html

```html
<div class="King_Chance_Layer">
    	<div class="King_Chance_LayerCont" style="display:none;">
        	<div class="King_Chance_Layer_Close">Close</div>
            <div class="King_Chance_Layer_Title">SHOPBEST 商城SHOPBEST 商城SHOPBEST 商城SHOPBEST 商城</div>
            <div class="King_Chance_Layer_Btn">
            	<ul>
                	<li><a href="#" title="百搭潮">百搭潮</a></li>
                    <li><a href="#" title="抗皱棉">抗皱棉</a></li>
                    <li><a href="#" title="植绒">植绒</a></li>
                    <li><a href="#" title="潮范">潮范</a></li>
                </ul>
            </div>
            <div class="King_Chance_Layer_Content">
            	<ul>
                	<li><a href="#" title="百搭潮"><img src="/static/images/King_imgs/ipush1.jpg" alt="百搭潮"></a></li>
                    <li><a href="#" title="抗皱棉"><img src="/static/images/King_imgs/ipush2.jpg" alt="抗皱棉"></a></li>
                    <li><a href="#" title="植绒"><img src="/static/images/King_imgs/ipush3.jpg" alt="植绒"></a></li>
                    <li><a href="#" title="潮范"><img src="/static/images/King_imgs/ipush4.jpg" alt="潮范"></a></li>
                </ul>
            </div>
        </div>
    </div>
</div>
```

最后只需要在需要的页面添加如下代码就行

```html
{% module Advertisement() %}<br>
```



最后在模板还提供了一些其他的功能

**set设置局部变量**

```html
<!--通过set设置局部变量-->
{% set su = Count().sum %}
{{ su(6,9) }} <br>

{% set args = Count().args %}
{% for a in args(1,2,3,4,5) %}
    {{ a }}<br>
{% end %}
```

**使用apply语句，使用函数的作用范围到最近的{%end%}为止**

```html
{% apply upper %}
    hello world<br>
    hahaha
{% end %}
{{ upper('hahaha') }} <br>
```

**linkify生成一个链接**

```html
{{ linkify('百度: http://www.baidu.com') }} <br>
{%raw linkify('百度: http://www.baidu.com') %}
```

