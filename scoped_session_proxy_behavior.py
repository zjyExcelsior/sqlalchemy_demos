# coding: utf-8
"""SQLAlchemy scoped_session proxy behavior demo"""
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

connect_params = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'testonly',
    'password': 'testonly',
    'host': 'localhost',
    'port': 3306,
    'database': 'comment_demo'
}
DB_URI = ('{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
          '?charset=utf8').format(**connect_params)
engine = create_engine(DB_URI, echo=False)
# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)
# mapped classes are now created with names by default
# matching that of the table name.
User = Base.classes.users

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

USER_NAME = 'testonly_for_it'
NEW_PASS = 'new_passowrd'


def print_session_id():
    print('Session id: %s', id(Session))
    print('session id: %s', id(Session()))
    print('------------------')


def add_users():
    print_session_id()
    user = User(name=USER_NAME, password='123')
    Session.add(user)
    Session.commit()
    Session.remove()


def delete_user(user_name):
    print_session_id()
    Session.query(User).filter_by(name=user_name).delete()
    Session.commit()
    Session.remove()


def modify_user(new_password):
    print_session_id()
    Session.query(User).update({'password': new_password})
    Session.commit()
    Session.remove()


def list_users():
    print_session_id()
    users = Session.query(User).all()
    Session.remove()
    return users


if __name__ == '__main__':
    add_users()
    modify_user(NEW_PASS)
    print(list_users())
    delete_user(USER_NAME)
