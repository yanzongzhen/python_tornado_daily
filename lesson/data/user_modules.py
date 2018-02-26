from datetime import datetime

from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey

from .connect import Base, session
# import sys
# sys.path.append('../')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),nullable=False)
    password = Column(String(50))
    creatime = Column(DateTime,default=datetime.now)
    _locked = Column(Boolean,default=False,nullable=False)

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

    @locked.setter
    def locked(self,value):
        assert isinstance(value,bool)
        self._locked = value

    def __repr__(self):
        return "<User(id='%s',username='%s',password='%s',creatime='%s',_locked='%s')>"%(
            self.id,
            self.username,
            self.password,
            self.creatime,
            self._locked
        )

class UserDetails(Base):
    __tablename__='user_details'
    id = Column(Integer,primary_key=True,autoincrement=True)
    id_card = Column(Integer,nullable=True,unique=True)
    lost_login = Column(DateTime)
    login_num = Column(Integer,default=0)
    user_id = Column(Integer,ForeignKey('user.id'))

    userdetail_for_foreignkey = relationship('User',backref='details',uselist=False,cascade='all')

    def __repr__(self):
        return '<UserDetails(id=%s,id_card=%s,last_login=%s,login_num=%s,user_id=%s)>'%(
            self.id,
            self.id_card,
            self.lost_login,
            self.login_num,
            self.user_id
        )



if __name__=='__main__':
    Base.metadata.create_all()
