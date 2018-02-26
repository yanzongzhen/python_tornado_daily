from user_modules import User,session

def add_user():
    # person = User(username='wawa',password='qwe123')
    # session.add(person)

    session.add_all([User(username='wangshouyuan',password='123'),
                    User(username='houguanglong', password='qwe')]
                    )

    session.commit()


def search_user():
    row = session.query(User).all()
    # print(row)
    row = session.query(User).filter_by(id=1).all()
    # print(row)

    row = session.query(User).filter(User.username=='wangshouyuan').all()
    print(row[0].locked)

def update_user():
    row = session.query(User).filter_by(username='houguanglong').update({User.password:'QWE'})
    session.commit()

def delete_user():
    row = session.query(User).filter_by(username='houguanglong')[0]  #first
    print(row)
    session.delete(row)
    session.commit()


if __name__=='__main__':
    # add_user()
    # search_user()
    # update_user()
    # delete_user()
    # print(User.all())
    # print(User.by_id(1))
    # print(User.by_name('houguanglong'))
    print(User.by_name('houguanglong'))
