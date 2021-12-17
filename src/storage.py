import pickle
import json
import os


class Land(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.rarity = kwargs.get('rarity')
        self.lvl = kwargs.get('lvl')
        self.fee = kwargs.get('fee')
        self.xps_ph = kwargs.get('xps_ph', None)
        self.bmtl_ph = kwargs.get('bmtl_ph', None)
        self.lsm_ph = kwargs.get('lsm_ph', None)
        self.mnrl_ph = kwargs.get('mnrl_ph', None)
        self.ocp_ph = kwargs.get('ocp_ph', None)
        self.ree_ph = kwargs.get('ree_ph', None)
        self.equipment_1 = kwargs.get('equipment_1', None)
        self.equipment_2 = kwargs.get('equipment_2', None)
        self.equipment_3 = kwargs.get('equipment_3', None)
        self.equipment_4 = kwargs.get('equipment_4', None)
        self.next_work_wait_time = kwargs.get('next_work_wait_time', None)

    def __repr__(self):
        return f"<Land(" \
               f"name: {self.name}, " \
               f"rarity: {self.rarity}, " \
               f"lvl: {self.lvl}, " \
               f"fee: {self.fee}, " \
               f"xps_ph: {self.xps_ph}, " \
               f"bmtl_ph: {self.bmtl_ph}, " \
               f"mnrl_ph: {self.mnrl_ph}, " \
               f"ocp_ph: {self.ocp_ph}, " \
               f"ree_ph: {self.ree_ph}, " \
               f"equipment_1: {self.equipment_1}, " \
               f"equipment_2: {self.equipment_2}, " \
               f"equipment_3: {self.equipment_3}, " \
               f"equipment_4: {self.equipment_4}, " \
               f"next_work_wait_time: {self.next_work_wait_time})>"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Account:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.session_token = kwargs.get('session_token', None)
        self.session_id = kwargs.get('session_id', None)
        self.token_upd_time = kwargs.get('token_upd_time', None)
        self.login_fail = kwargs.get('login_fail', 0)
        self.lands = kwargs.get('lands', {})
        self.xps = kwargs.get('xps', None)
        self.bmtl = kwargs.get('bmtl', None)
        self.lsm = kwargs.get('lsm', None)
        self.mnrl = kwargs.get('mnrl', None)
        self.ocp = kwargs.get('ocp', None)
        self.ree = kwargs.get('ree', None)
        self.next_work_wait_time = kwargs.get('next_work_wait_time', None)

    def __repr__(self):
        return f"<Account(" \
               f"name: {self.name}, " \
               f"session_token: {self.session_token}, " \
               f"session_id: {self.session_id}, " \
               f"lands: {self.lands}, " \
               f"token_upd_time: {self.token_upd_time}, " \
               f"login_fail: {self.login_fail}, " \
               f"xps: {self.xps}, " \
               f"bmtl: {self.bmtl}, " \
               f"lsm: {self.lsm}, " \
               f"mnrl: {self.mnrl}, " \
               f"ocp: {self.ocp}, " \
               f"ree: {self.ree}, " \
               f"next_work_wait_time: {self.next_work_wait_time})>"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add_land(self, land):
        self.lands.update(json.loads(land.toJSON()))


class PklStorage:
    def __load(self):
        with open('.pklstor', 'rb') as handle:
            data = pickle.load(handle)
        return data

    def __save(self, data):
        with open('.pklstor', 'wb+') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def get_account(self, name):
        if not os.path.exists('.pklstor'):
            return None
        now_data = self.__load()
        if name in now_data:
            return now_data[name]

    def add_account(self, account):
        if os.path.exists('.pklstor'):
            now_data = self.__load()
        else:
            now_data = {}
        now_data[account['name']] = account
        self.__save(now_data)

    def update_account(self, account):
        now_data = self.__load()
        now_data[account['name']].update(account)
        self.__save(now_data)

    def get_all(self):
        return (i for i in self.__load().items())


class CredStorage:
    def __load(self):
        with open('.credstor', 'rb') as handle:
            data = pickle.load(handle)
        return data

    def __save(self, data):
        with open('.credstor', 'wb+') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def get_account(self, name):
        if not os.path.exists('.credstor'):
            return None
        now_data = self.__load()
        if name in now_data:
            return now_data[name]

    def add_account(self, account):
        if os.path.exists('.credstor'):
            now_data = self.__load()
        else:
            now_data = {}
        now_data[account['name']] = account
        self.__save(now_data)

    def update_account(self, account):
        now_data = self.__load()
        now_data[account['name']].update(account)
        self.__save(now_data)