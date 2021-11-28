import logging
import os

from sqlalchemy import Column, Integer, String, ForeignKey, REAL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column('name', String, unique=True, nullable=False)
    session_token = Column('session_token', String)
    session_id = Column('session_id', String)
    token_upd_time = Column('token_upd_time', Integer)
    login_fail = Column('login_fail', Integer)
    xps = Column('xps', REAL)
    bmtl = Column('bmtl', REAL)
    lsm = Column('lsm', REAL)
    mnrl = Column('mnrl', REAL)
    ocp = Column('ocp', REAL)
    ree = Column('ree', REAL)
    next_mining_time = Column('next_mining_time', Integer)
    worth_rest = Column('worth_rest', Integer)
    next_work_time = Column('next_work_time', Integer)

    def __init__(self,
                 name,
                 session_token=None,
                 session_id=None,
                 token_upd_time=None,
                 login_fail=None,
                 xps=None,
                 bmtl=None,
                 lsm=None,
                 mnrl=None,
                 ocp=None,
                 ree=None,
                 next_mining_time=None,
                 worth_rest=None,
                 next_work_time=None):
        self.name = name
        self.session_token = session_token
        self.session_id = session_id
        self.token_upd_time = token_upd_time
        self.login_fail = login_fail
        self.xps = xps
        self.bmtl = bmtl
        self.lsm = lsm
        self.mnrl = mnrl
        self.ocp = ocp
        self.ree = ree
        self.next_mining_time = next_mining_time
        self.worth_rest = worth_rest
        self.next_work_time = next_work_time

    def __repr__(self):
        return f"<Account(name: {self.name}, session_token: {self.session_token}, session_id: {self.session_id}, " \
               f"token_upd_time: {self.token_upd_time}, login_fail: {self.login_fail}, wood: {self.wood}, " \
               f"gold: {self.gold}, food: {self.food}, energy: {self.energy}, next_mining_time: {self.next_mining_time}," \
               f" worth_rest: {self.worth_rest}, next_work_time: {self.next_work_time})>"


class Land(Base):
    __tablename__ = 'lands'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    rarity = Column('rarity', String)
    lvl = Column('lvl', REAL)
    xps_ph = Column('xps_ph', REAL)
    bmtl_ph = Column('bmtl_ph', REAL)
    lsm_ph = Column('lsm_ph', REAL)
    mnrl_ph = Column('mnrl_ph', REAL)
    ocp_ph = Column('ocp_ph', REAL)
    ree_ph = Column('ree_ph', REAL)
    equipment_1 = Column('equipment_1', String)
    equipment_2 = Column('equipment_2', String)
    equipment_3 = Column('equipment_3', String)
    equipment_4 = Column('equipment_4', String)
    fee = Column('fee', REAL)
    next_mining_time = Column('next_mining_time', REAL)
    account_id = Column('account_id', Integer, ForeignKey("accounts.id"))

    def __init__(self,
                 name,
                 rarity,
                 lvl,
                 fee,
                 account_id,
                 xps_ph=None,
                 bmtl_ph=None,
                 lsm_ph=None,
                 mnrl_ph=None,
                 ocp_ph=None,
                 ree_ph=None,
                 equipment_1=None,
                 equipment_2=None,
                 equipment_3=None,
                 equipment_4=None,
                 next_mining_time=None):
        self.name = name,
        self.rarity = rarity,
        self.lvl = lvl
        self.fee = fee
        self.xps_ph = xps_ph
        self.bmtl_ph = bmtl_ph
        self.lsm_ph = lsm_ph
        self.mnrl_ph = mnrl_ph
        self.ocp_ph = ocp_ph
        self.ree_ph = ree_ph
        self.equipment_1 = equipment_1
        self.equipment_2 = equipment_2
        self.equipment_3 = equipment_3
        self.equipment_4 = equipment_4
        self.next_mining_time = next_mining_time
        self.account_id = account_id

        logging.info(f"LAND NAME: {name} {type(name)}")
        logging.info(f"LAND RARITY: {rarity} {type(rarity)}")

    def __repr__(self):
        return f"<Land(name: {self.name}, rarity: {self.rarity}, " \
               f"lvl: {self.lvl}, " \
               f"fee: {self.fee}, " \
               f"account_id: {self.account_id}, " \
               f"xps_ph: {self.xps_ph}, " \
               f"bmtl_ph: {self.bmtl_ph}, " \
               f"mnrl_ph: {self.mnrl_ph}, " \
               f"ocp_ph: {self.ocp_ph}, " \
               f"ree_ph: {self.ree_ph}, " \
               f"equipment_1: {self.equipment_1}, " \
               f"equipment_2: {self.equipment_2}, " \
               f"equipment_3: {self.equipment_3}, " \
               f"equipment_4: {self.equipment_4}, " \
               f"next_mining_time: {self.next_mining_time})>"


class Claim(Base):
    __tablename__ = 'claims'
    id = Column('id', Integer, primary_key=True)
    timestamp = Column('timestamp', Integer, nullable=False)
    net = Column('net', REAL, nullable=False)
    land_id = Column('land_id', Integer, ForeignKey("lands.id"))

    def __init__(self, timestamp, xps_net, bmtl_net, mnrl_net, ocp_net, ree_net, land_id):
        self.timestamp = timestamp
        self.xps_net = xps_net
        self.bmtl_net = bmtl_net
        self.mnrl_net = mnrl_net
        self.ocp_net = ocp_net
        self.ree_net = ree_net
        self.land_id = land_id

    def __repr__(self):
        return f"<Claim(name: {self.name}, timestamp: {self.timestamp}, " \
               f"xps_net: {self.net}, bmtl_net: {self.bmtl_net}, mnrl_net: {self.mnrl_net}, ocp_net: {self.ocp_net}, ree_net: {self.ree_net}, " \
               f"land_id: {self.account_id})>"


class Storage:
    def __init__(self, db_path, db_name):
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        self.engine = create_engine(f'sqlite:///{os.path.join(db_path, db_name)}')
        Base.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)()

    def add_account(self, account):
        self.session.add(account)
        self.session.commit()

    def get_account(self, name):
        for account in self.session.query(Account).order_by(Account.id):
            if account.name == name:
                return account
        return None

    def update_account(self,
                       src_name,
                       name=None,
                       session_token=None,
                       session_id=None,
                       token_upd_time=None,
                       login_fail=None,
                       xps=None,
                       bmtl=None,
                       lsm=None,
                       mnrl=None,
                       ocp=None,
                       ree=None,
                       next_mining_time=None,
                       worth_rest=None,
                       next_work_time=None, ):
        old_account = self.get_account(src_name)

        self.session.query(Account).filter(Account.name == src_name).update(
            {
                Account.name: name if name else old_account.name,
                Account.session_token: session_token if session_token else old_account.session_token,
                Account.session_id: session_id if session_id else old_account.session_id,
                Account.token_upd_time: token_upd_time if token_upd_time else old_account.token_upd_time,
                Account.login_fail: login_fail if login_fail else old_account.login_fail,
                Account.xps: xps if xps else old_account.xps,
                Account.bmtl: bmtl if bmtl else old_account.bmtl,
                Account.lsm: lsm if lsm else old_account.lsm,
                Account.mnrl: mnrl if mnrl else old_account.mnrl,
                Account.ocp: ocp if ocp else old_account.ocp,
                Account.ree: ree if ree else old_account.ree,
                Account.next_mining_time: next_mining_time if next_mining_time else old_account.next_mining_time,
                Account.worth_rest: worth_rest if worth_rest else old_account.worth_rest,
                Account.next_work_time: next_work_time if next_work_time else old_account.next_work_time
            }
        )
        self.session.commit()

    def add_land(self, land):
        self.session.add(land)
        self.session.commit()

    def get_land(self, name, account_id):
        for land in self.session.query(Land).order_by(Land.id):
            if land.name == name and land.account_id == account_id:
                return land
        return None

    def update_land(self,
                    src_name,
                    account_id,
                    name=None,
                    rarity=None,
                    lvl=None,
                    fee=None,
                    xps_ph=None,
                    bmtl_ph=None,
                    lsm_ph=None,
                    mnrl_ph=None,
                    ocp_ph=None,
                    ree_ph=None,
                    equipment_1=None,
                    equipment_2=None,
                    equipment_3=None,
                    equipment_4=None,
                    next_mining_time=None):
        old_land = self.get_land(src_name, account_id)

        self.session.query(Land).filter(Land.name == src_name and Land.account_id == account_id).update(
            {
                Land.name: name if name else old_land.name,
                Land.rarity: rarity if rarity else old_land.rarity,
                Land.lvl: lvl if lvl else old_land.lvl,
                Land.fee: fee if fee else old_land.fee,
                Land.xps_ph: xps_ph if xps_ph else old_land.xps_ph,
                Land.bmtl_ph: bmtl_ph if bmtl_ph else old_land.bmtl_ph,
                Land.lsm_ph: lsm_ph if lsm_ph else old_land.lsm_ph,
                Land.mnrl_ph: mnrl_ph if mnrl_ph else old_land.mnrl_ph,
                Land.ocp_ph: ocp_ph if ocp_ph else old_land.ocp_ph,
                Land.ree_ph: ree_ph if ree_ph else old_land.ree_ph,
                Land.equipment_1: equipment_1 if equipment_1 else old_land.equipment_1,
                Land.equipment_2: equipment_2 if equipment_2 else old_land.equipment_2,
                Land.equipment_3: equipment_3 if equipment_3 else old_land.equipment_3,
                Land.equipment_4: equipment_4 if equipment_4 else old_land.equipment_4,
                Land.next_mining_time: next_mining_time if next_mining_time else old_land.next_mining_time
            }
        )
        self.session.commit()

    def add_claim(self, claim):
        self.session.add(claim)
        self.session.commit()
