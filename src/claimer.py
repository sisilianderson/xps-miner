import logging
import time

from selenium.webdriver.common.by import By

from utils import is_popup_window, switch_to_popup_wnd, switch_to_wnd, get_current_wnd
from storage import PklStorage


class ClaimXPS:
    def __init__(self, account, config, driver, rent):
        self.account = account
        self.config = config
        self.driver = driver
        self.db = PklStorage()
        self.login_to_game()
        self.rent = rent

    def login_to_game(self):
        self.driver.get("https://play.xpsgame.io")
        time.sleep(5)

        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[2]/div/div[2]/button[1]').click()

        main_wnd = get_current_wnd(self.driver)
        if is_popup_window(self.driver):
            switch_to_popup_wnd(self.driver)
            time.sleep(3)
            self.driver.find_element_by_xpath(
                '/html/body/div/div/section/div[2]/div/div[6]/button').click()
            switch_to_wnd(self.driver, main_wnd)
        time.sleep(10)

    def get_account_resources(self):
        xps = self.driver.find_element(by=By.XPATH,
                                       value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div[1]/span[2]').text
        bmtl = self.driver.find_element(by=By.XPATH,
                                        value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div[2]/span[2]').text
        lsm = self.driver.find_element(by=By.XPATH,
                                       value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div[3]/span[2]').text
        mnrl = self.driver.find_element(by=By.XPATH,
                                        value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div[4]/span[2]').text
        ocp = self.driver.find_element(by=By.XPATH,
                                       value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div[5]/span[2]').text
        ree = self.driver.find_element(by=By.XPATH,
                                       value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div[6]/span[2]').text

        return {'xps': xps, 'bmtl': bmtl, 'lsm': lsm, 'mnrl': mnrl, 'ocp': ocp, 'ree': ree}

    def get_account_lands(self):
        res = {}
        lands_container = self.driver.find_element(by=By.XPATH,
                                                   value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div')
        land_index = 0
        for div in lands_container.find_elements_by_tag_name('div'):
            if 'land-card' in div.get_attribute("class"):
                logging.info("Land --")
                land_index += 1
                try:
                    land_id = self.driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[1]/span[1]').text
                    res[land_id] = {}

                    rare = self.driver.find_element(by=By.XPATH,
                                                    value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[1]/span[2]').text

                    xps_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[1]/span[2]').text

                    bmtl_ph = self.driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[2]/span[2]').text

                    lsm_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[3]/span[2]').text

                    mnrl_ph = self.driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[4]/span[2]').text

                    ocp_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[5]/span[2]').text

                    ree_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[6]/span[2]').text

                    try:
                        wait_time = self.driver.find_element(by=By.XPATH,
                                                             value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[4]/div/div/button/p').text
                        logging.info(
                            f"ID: {land_id}, RARE: {rare}, XPS_PH: {xps_ph}, BMTL_PH: {bmtl_ph}, LSM_PH: {lsm_ph}, MNRL_PH: {mnrl_ph}, OCP_PH: {ocp_ph}, REE_PH: {ree_ph}, wait_time: {wait_time}")
                    except Exception:
                        wait_time = 0
                except Exception:
                    continue
                res[land_id] = {"name": land_id, "rare": rare, "lvl": 1, "fee": 20, 'xps_ph': xps_ph,
                                'bmtl_ph': bmtl_ph, 'lsm_ph': lsm_ph, 'mnrl_ph': mnrl_ph, 'ocp_ph': ocp_ph,
                                'ree_ph': ree_ph, 'next_work_wait_time': wait_time}
        return res

    def get_rent_lands(self):
        res = {}
        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/button[2]').click()
        time.sleep(5)
        lands_container = self.driver.find_element(by=By.XPATH,
                                                   value='/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div')

        land_index = 0
        for div in lands_container.find_elements_by_tag_name('div'):
            if 'land-card' in div.get_attribute("class"):
                logging.info("Land --")
                land_index += 1
                try:
                    land_id = self.driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[1]/span[1]').text
                    res[land_id] = {}

                    rare = self.driver.find_element(by=By.XPATH,
                                                    value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[1]/span[2]').text

                    xps_ph = 0

                    bmtl_ph = self.driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[1]/span[2]').text

                    lsm_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[2]/span[2]').text

                    mnrl_ph = self.driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[3]/span[2]').text

                    ocp_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[4]/span[2]').text

                    ree_ph = self.driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[3]/div[5]/span[2]').text

                    try:
                        wait_time = self.driver.find_element(by=By.XPATH,
                                                             value=f'/html/body/div[1]/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[{land_index}]/div/div[4]/div/div/button/p').text
                        logging.info(f"ID: {land_id}, RARE: {rare}, XPS_PH: {xps_ph}, BMTL_PH: {bmtl_ph}, LSM_PH: {lsm_ph}, MNRL_PH: {mnrl_ph}, OCP_PH: {ocp_ph}, REE_PH: {ree_ph}, wait_time: {wait_time}")
                    except Exception:
                        wait_time = 0
                except Exception:
                    continue
                res[land_id] = {"name": land_id, "rare": rare, "lvl": 1, "fee": 20, 'xps_ph': xps_ph,
                                'bmtl_ph': bmtl_ph, 'lsm_ph': lsm_ph, 'mnrl_ph': mnrl_ph, 'ocp_ph': ocp_ph,
                                'ree_ph': ree_ph, 'next_work_wait_time': wait_time}

        return res

    def claim_land(self):
        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div[2]/div/div[3]/div/div[1]/div/div[1]/div[8]/button').click()
        time.sleep(3)

        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/button[2]').click()
        time.sleep(10)

        main_wnd = get_current_wnd(self.driver)
        if is_popup_window(self.driver):
            switch_to_popup_wnd(self.driver)
            time.sleep(10)
            self.driver.find_element_by_xpath(
                '/html/body/div/div/section/div[2]/div/div[5]/button/div').click()
            switch_to_wnd(self.driver, main_wnd)
        if self.rent:
            time.sleep(60)
        else:
            time.sleep(5)

        try:
            res_txt = self.driver.find_element(by=By.XPATH,
                                               value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[2]/div').text
            logging.info(f"Claim text: {res_txt}")
            self.driver.find_element(by=By.XPATH,
                                     value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/button').click()
        except Exception:
            pass

        try:
            self.driver.find_element(by=By.XPATH,
                                     value='/html/body/div[1]/div/div/div/div[1]/div/div[3]/button').click()
        except Exception:
            pass

    def claim_xps(self):
        account_res = self.get_account_resources()
        account_lands = self.get_account_lands() if not self.rent else self.get_rent_lands()

        if not self.db.get_account(self.account):
            a = {'name': self.account}
            a.update(account_res)
            a.update({"lands": account_lands})
            self.db.add_account(a)
        else:
            a = {'name': self.account}
            a.update(account_res)
            a.update({"lands": account_lands})
            self.db.update_account(a)

        if all(v == 0 for v in [account_lands[land]['next_work_wait_time'] for land in account_lands]):
            self.claim_land()

            account_res = self.get_account_resources()
            account_lands = self.get_account_lands() if not self.rent else self.get_rent_lands()
            a = {'name': self.account}
            a.update(account_res)
            a.update({"lands": account_lands})
            self.db.update_account(a)
            return True
        return False

    def claim_stake(self):
        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/a[4]/button').click()
        time.sleep(5)
        claim_button = self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div[3]/div[3]/button')
        if claim_button.text.strip() == "Claim x6":
            logging.info(f"CLAIM BUTTON: {claim_button.text}")
            claim_button.click()

        time.sleep(2)
        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/button[2]').click()
        time.sleep(3)

        main_wnd = get_current_wnd(self.driver)
        if is_popup_window(self.driver):
            switch_to_popup_wnd(self.driver)
            time.sleep(10)
            self.driver.find_element_by_xpath(
                '/html/body/div/div/section/div[2]/div/div[5]/button/div').click()
            switch_to_wnd(self.driver, main_wnd)

        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[1]/div/div[3]/button').click()

        self.driver.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div/div[2]').click()

        time.sleep(5)