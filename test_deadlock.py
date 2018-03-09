# coding=utf-8
import threading
import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

Base = declarative_base()


class MyTable(Base):
    __tablename__ = 'mytable'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(60), unique=True, nullable=False)


e = create_engine("mysql://testonly:testonly@localhost/comment_demo",
                  echo=True)
Base.metadata.drop_all(e)
Base.metadata.create_all(e)

s = Session(e)
print('main_thread session id: %s', id(s))
s.begin_nested()
s.add(MyTable(name='mitsos'))
s.flush()
print('after main_thread session flush')


def go():
    s2 = Session(e)
    print('thread t session id: %s', id(s2))
    s2.begin_nested()
    print('after s2 begin_nested')
    s2.add(MyTable(name='mitsos'))
    print('after s2 add')
    try:
        s2.flush()
        print('after s2 flush')
    except Exception as err:
        print('->exception: {}'.format(err))
        try:
            s2.rollback()
        except Exception:
            print('->rollback error')
        print('->after rollback')


t = threading.Thread(target=go)
t.start()
time.sleep(2)

print('after t.start()')
s.add(MyTable(name='mit'))
s.flush()
print('before main_thread commit')
s.commit()
print('after main_thread commit')
