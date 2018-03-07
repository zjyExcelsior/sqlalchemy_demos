# coding: utf-8
"""SQLAlchemy only_return_tuples demo

Test new feature in 1.2.5: Query.only_return_tuples()
"""
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

Session = sessionmaker(bind=engine)


def add_users():
    s = Session()
    user_a = User(name='testonly_for_it', password=123)
    s.add(user_a)
    s.commit()


def delete_users():
    s = Session()
    s.query(User).filter_by(name='testonly_for_it').delete()
    s.commit()


def get_user():
    s = Session()
    query = s.query(User).filter_by(name='testonly_for_it')
    query = query.only_return_tuples(True)
    user = query.first()
    assert isinstance(user, tuple)
    return user


if __name__ == '__main__':
    add_users()
    print(get_user())
    delete_users()
