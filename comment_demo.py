# coding: utf-8
"""SQLAlchemy comment demo

new in version 1.2
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

connect_params = {
    'dialect': 'mysql',
    'driver': 'mysqldb',
    'username': 'root',
    'password': 'zhujiongyao',
    'host': 'localhost',
    'port': 3306,
    'database': 'comment_demo'
}
DB_URI = ('{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
          '?charset=utf8').format(**connect_params)

engine = create_engine(DB_URI, echo=False)
Base = declarative_base()


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_tables(engine):
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), comment='my name')
    password = Column(String(20), comment='my password')

    def __repr__(self):
        return '<User(name="%s", password="%s")>' % (self.name, self.password)


if __name__ == '__main__':
    drop_tables(engine)
    create_tables(engine)
