# SQLAlchemy

##### 1.环境搭建

##### 2.连接数据库

##### 3.创建模型



 ### 1.环境搭建

安装相应的软件包

1.`mysql`数据库

2.`pymysql`用于连接`MySQL`服务器的一个库

3.`sqlalchemy`

```shell
$ pip install pymysql
$ pip install sqlalchemy
```



### 2.连接数据库

从sqlalchemy中导入create_engin，创建引擎建立与数据库的连接。

`from sqlalchemy import create_engine`

准备连接数据库的数据：
HOSTNAME = '127.0.0.1'        # ip地址
PORT = '3306'                          # 端口号
DATABASE = 'mydb'                # 数据库名
USERNAME = 'admin'                 # 用户名
PASSWORD = 'rootqwe123'                 # 用户登录密码

DB_URI的格式:
数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名?字符编码
DB_URI=`mysql+pymysql://<username>:<password>@<host>/<dbname>?charset=utf8` 

engine = create_engine(DB_URI)

我们可以尝试着测试一下是否连接上:

`print(dir(engine))`,当有打印出方法时，表示连接成功。

```python
#connect.py
from sqlalchemy import create_engine

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

Db_Uri = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,DATABASE)

engine = create_engine(Db_Uri)

if __name__=='__main__':
    print(dir(engine))
```



### 3.创建模型

**声明映像**

对象关系型映射，数据库中的表与python中的类相对应，创建的类必须继承自sqlalchemy中的基类。

使用Declarative方法定义的映射类依据一个基类，这个基类是维系类和数据表关系的目录。
应用通常只需要有一个base的实例。我们通过declarative_base()功能创建一个基类。

```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)
```

**创建会话**

定义个`session`会话对象,使用 `sessionmaker`初始化一个类对象

```python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()
```

**新建模型**

新建一个user模型

```python
import datetime
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from connect import Base,session

class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),nullable=False)
    password = Column(String(100))
    creatime = Column(DateTime,default=datetime.now)
    last_login = Column(DateTime)
    _locked = Column(Boolean,default=Falsem,nullable=False)
    
#---将创建好的user类，映射到数据库的user表中---
Base.metadata.create_all()    
```

这就是创建好了一个表，我们可以在数据库中查看一下。

现在是往表里面添加数据：

```python
def add_user():
	#添加单个对象
	#person = User(name='budong',number=11)
	#session.add(person)

	#添加多个对象
	session.add_all([User(name='tuple',number=2),\
	        User(name='which',number=3)])
	#提交才会生效，和命令行有区别
	session.commit()
add_user()
```

接下来是查询数据

```python
def search_user():
    row = session.query(User).all()
    # print(row)
    row = session.query(User).filter_by(id=1).all()
    # print(row)

    row = session.query(User).filter(User.username=='wangshouyuan').all()
    print(row[0].locked)
```

但其实我们可以在定义user类的时候这么去写

```python
    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def by_id(cls,id):
        return session.query(cls).filter_by(id=id).all()

    @classmethod
    def by_name(cls,name):
        return session.query(cls).filter_by(username=name).all()

    @property
    def locked(self):
        return self._locked
```

这样在只需要调用类方法就行

```python
    print(User.all())
    print(User.by_id(1))
    print(User.by_name('budong'))
    print(User.by_name('budong'))
```

更新

```python
def update_user():
    row = session.query(User).filter_by(username='houguanglong').update({User.password:'QWE'})
    session.commit()
```

删除

```python
def delete_user():
    row = session.query(User).filter_by(username='houguanglong')[0]  #first
    print(row)
    session.delete(row)
    session.commit()
```

以上就是sqlalchemy的基本知识。

