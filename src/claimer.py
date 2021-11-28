import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from database import Claim, Land
from utils import is_popup_window, switch_to_popup_wnd, switch_to_wnd, get_current_wnd
from clicker import MockClicker


class ClaimXPS:
    def __init__(self, account, config, driver, db):
        self.account = account
        self.config = config
        self.driver = driver
        self.db = db
        self.clicker = MockClicker(self.account)

    def __lands_info(self):
        res = {}
        for land in self.clicker.get_account_lands():
            res[land] = {}
            res[land].update(self.clicker.get_land_ph(land))
            res[land].update({'next_work_wait_time': self.clicker.get_land_wait_time(land)})
            res[land].update(self.clicker.get_land_equipments(land))
            res[land].update({'fee': self.clicker.get_land_fee(land)})
        return res

    def claim_xps(self):

        account_res = self.clicker.get_account_resources()
        account_lands = self.__lands_info()
        if not self.db.get_account(self.account):
            a = {'name': self.account}
            a.update(account_res)
            a.update({"lands": account_lands})
            self.db.add_account(a)

        for land in account_lands:
            if account_lands[land]['next_work_wait_time'] == 0:
                self.clicker.claim_land(land)

        account_res = self.clicker.get_account_resources()
        account_lands = self.__lands_info()
        a = {'name': self.account}
        a.update(account_res)
        a.update({"lands": account_lands})
        self.db.update_account(a)
