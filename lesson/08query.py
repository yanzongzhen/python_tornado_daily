from data.user_modules import User,session,UserDetails

#带条件查询
row = session.query(User).filter_by(username='wawa').all()
# print(row)
# print( session.query(User).filter(User.username=='wawa').all() )
# print( session.query(User).filter(User.username!='wawa').all() )
# print( session.query(User).filter(User.username!='wawa') )
# print( session.query(User).all() )
# print( session.query(User.username).filter(User.username!='wawa').all() )

#
# print( session.query(User).filter(User.username!='wawa').first() )
# print( session.query(User.username).filter(User.username!='wawa').one() )
# print( session.query(User).get(2))  #根据主键去查

#限制查询结果数
# print( session.query(User.username).filter(User.username!='wawa').all() )
# print( session.query(User.username).filter(User.username!='wawa').limit(3).all() )
# print( session.query(User.username).filter(User.username!='wawa').offset(3).all() )
# print( session.query(User.username).filter(User.username!='wawa').slice(1,3).all() )

from sqlalchemy import desc
# print( session.query(User.username).filter(User.username!='wawa').order_by(User.id).all() )
# print( session.query(User.username).filter(User.username!='wawa').order_by(User.username).limit(3).all() )
# print( session.query(User.username).filter(User.username!='wawa').order_by(desc(User.username)).all() )

#模糊匹配
# print( session.query(User.username).filter(User.username!='wawa').all )
# print( session.query(User.username).filter(User.username.like('w%')).all() )
# print( session.query(User.username).filter(User.username.notlike('w%')).all() )
# print( session.query(User.username).filter(User.username.in_(['budong','wawa'])).all() )
# print( session.query(User.username).filter(User.username.notin_(['budong','wawa'])).all() )

# print( session.query(User.username).filter(User.username==None).all() )
# print( session.query(User.username).filter(User.username.is_(None)).all() )
# print( session.query(User.username).filter(User.username.isnot(None),User.password=='qwe123').all() )

from sqlalchemy import or_
# print( session.query(User.username).filter(or_(User.username.isnot(None),User.password=='qwe123')).all() )

#聚合函数
from sqlalchemy import func,extract
# print( session.query(User.password,func.count(User.id)).group_by(User.password).all() )
# print( session.query(User.password,func.count(User.id)).group_by(User.password).\
#        having(func.count(User.id)>1).all() )

# print( session.query(User.password,func.sum(User.id)).group_by(User.password).all() )
# print( session.query(User.password,func.max(User.id)).group_by(User.password).all() )
# print( session.query(User.password,func.min(User.id)).group_by(User.password).all() )
#
# print( session.query(extract('minute',User.creatime).label('minute'),\
#                      func.count(User.id)).group_by('minute').all() )
# print( session.query(extract('day',User.creatime).label('day'),\
#                      func.count('*')).group_by('day').all() )

#多表查询
# print( session.query(UserDetails).all() )
# print( session.query(User).all() )
# print( session.query(UserDetails,User).all() )
# print( session.query(UserDetails,User) )  #cross join
# print( session.query(UserDetails,User).filter(UserDetails.id==User.id).all() )  #
# print( session.query(UserDetails,User).filter(UserDetails.id==User.id) )  #cross join
# print( session.query(User.username,UserDetails.lost_login).\
#        join(UserDetails,UserDetails.id==User.id) )  #inner join
# print( session.query(User.username,UserDetails.lost_login).\
#        outerjoin(UserDetails,UserDetails.id==User.id).all() )  #left join

q1 = session.query(User.id)
q2 = session.query(UserDetails.id)
# print(q1.union(q2).all())

from sqlalchemy import all_,any_
sql_0 = session.query(UserDetails.lost_login).subquery()
print( session.query(User).filter(User.creatime > all_(sql_0)).all() )
print( session.query(User).filter(User.creatime > any_(sql_0)).all() )

#原生sql
sql_1='''
    select * from `user`
'''
row = session.execute(sql_1)
# print(row,dir(row))
# print(row.fetchone())
# print(row.fetchmany())
# print(row.fetchall())

for i in row:
    pass
    # print(i)













