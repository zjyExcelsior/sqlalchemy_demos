# coding: utf-8
"""SQLAlchemy comment demo"""
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connect_params = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'root',
    'password': 'zhujiongyao',
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
    user_a = User(name='a', password=123)
    s.add(user_a)
    s.commit()


def list_users():
    s = Session()
    users = s.query(User.id, User.name, User.password).all()
    return users


if __name__ == '__main__':
    add_users()
    print(list_users())
