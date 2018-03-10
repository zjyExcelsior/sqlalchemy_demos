# coding=utf-8
"""SQLAlchemy transaction demos"""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

connect_params = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'testonly',
    'password': 'testonly',
    'host': 'localhost',
    'port': 3306,
    'database': 'transaction_demos'
}
DB_URI = ('{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
          '?charset=utf8').format(**connect_params)

engine = create_engine(DB_URI, pool_recycle=3600, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def session_scope():
    """Session使用入口"""
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_tables(engine):
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    card_nums = Column(Integer, default=0, server_default='0', doc='用户持有的卡的总数')

    def __repr__(self):
        return '<User(name="%s", card_nums="%s")>' % (self.name,
                                                      self.card_nums)


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    card_no = Column(String(64), unique=True)
    name = Column(String(64))
    user_id = Column(Integer, doc='owner id')

    def __repr__(self):
        return '<Card(card_no="%s", name="%s")>' % (self.card_no, self.name)


def add_users(session):
    """添加用户"""
    user_a = User(name='user_a')
    user_b = User(name='user_b')
    users = [user_a, user_b]
    session.add_all(users)
    session.commit()  # 提交事务
    user_ids = [user.id for user in users]
    return user_ids


def add_cards(session, card_no, card_name, user_id):
    """添加卡"""
    card_0001 = Card(card_no=card_no, name=card_name, user_id=user_id)
    session.add(card_0001)


def inc_card_num(session, user_id, num):
    """增加用户的card_nums"""
    user = session.query(User).filter_by(id=user_id).first()
    user.card_nums = user.card_nums + num


def add_users_and_cards():
    with session_scope() as session:
        user_ids = add_users(session)  # 一个事务结束了
        user_id_first = user_ids[0]
        # 第一条SQL语句，启动了一个新事务
        add_cards(session, card_no='0001', card_name='card_0001',
                  user_id=user_id_first)  # 添加第一张卡
        add_cards(session, card_no='0002', card_name='card_0002',
                  user_id=user_id_first)  # 添加第二张卡
        session.commit()  # 提交事务


def add_cards_for_user_a(card_no, card_name, num):
    """给user_a新增一张卡

    transaction1: cards表新增一条记录
    transaction2: users表中对应的user的card_nums加1
    """
    with session_scope() as session:
        # transaction 1
        user_a = session.query(User).filter_by(
            name='user_a').first()  # 第一条SQL语句，触发了一个transaction的开始
        add_cards(session, card_no=card_no, card_name=card_name,
                  user_id=user_a.id)
        session.commit()  # 提交transaction 1
        # transaction 2
        try:
            inc_card_num(session, user_a.id, num)
            session.commit()  # 提交transaction 2
        except Exception:
            session.rollback()  # 增加card_nums出现异常，该事务回滚
        return user_a.card_nums


def test_tran1_failure():
    """"transaction1: F"""
    try:
        add_cards_for_user_a(card_no='0001', card_name='card_0001', num=1)
    except IntegrityError:
        print('验证成功')
    else:
        print('验证失败')


def test_tran1_success_tran2_success():
    """transaction1: T, transaction2: T"""
    card_nums = add_cards_for_user_a(card_no='0003', card_name='card_0003',
                                     num=1)
    assert card_nums == 1


def test_tran1_success_tran2_failure():
    """transaction1: T, transaction2: F"""
    card_nums = add_cards_for_user_a(card_no='0004', card_name='card_0004',
                                     num='invalid')
    assert card_nums == 0


class AaBbCc(object):
    """AaBbCc"""
    aa = 123

    def test_it():
        pass


def call_func_that_takes_a_dict(*args, **kwargs):
    pass


if __name__ == '__main__':
    drop_tables(engine)
    create_tables(engine)
    # 准备数据: user_a, user_b, card_0001, card_0002
    add_users_and_cards()
    # 给user_a增加一张card
    test_tran1_failure()
    test_tran1_success_tran2_success()
    # test_tran1_success_tran2_failure()
