import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from database import Claim
from utils import is_popup_window, switch_to_popup_wnd, switch_to_wnd, get_current_wnd
from clicker import MockClicker


class ClaimXPS:
    def __init__(self, account, config, driver, db):
        self.account = account
        self.config = config
        self.driver = driver
        self.db = db

    def claim_xps(self):
        self.clicker = MockClicker(self.account)

    def claim_fwx(self, debug_mode=False):
        self.driver.get(self.config["game_path"])
        time.sleep(10)
        self.driver.find_element(by=By.XPATH, value="/html/body/div/div/div/div/button").click()
        time.sleep(3)
        self.driver.find_element(by=By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/button[1]").click()
        time.sleep(3)

        main_wnd = get_current_wnd(self.driver)
        if is_popup_window(self.driver):
            switch_to_popup_wnd(self.driver)
            time.sleep(3)
            self.driver.find_element(by=By.XPATH, value='/html/body/div/div/section/div[2]/div/div[6]/button').click()
            switch_to_wnd(self.driver, main_wnd)
        time.sleep(10)

        if debug_mode:
            input()

        while True:
            gold, wood, food, enrg = self.get_resources()
            try:
                self.db.update_account(self.account, gold=float(gold))
                self.db.update_account(self.account, wood=float(wood))
                self.db.update_account(self.account, food=float(food))
                self.db.update_account(self.account, energy=int(enrg))
            except Exception:
                pass
            logging.info(f"My resources:\n gold: {gold}\n wood: {wood}\n food: {food}\n enrg: {enrg}")

            time_to_wait = self.get_wait_time()
            hours = int(time_to_wait.split(":")[0])
            minutes = int(time_to_wait.split(":")[1])
            seconds = int(time_to_wait.split(":")[2])
            seconds_to_next_mine = hours * 60 * 60 + minutes * 60 + seconds
            logging.info(f"Seconds to next mine: {seconds_to_next_mine}")

            if seconds_to_next_mine == 0:
                time.sleep(10)

                button = self.driver.find_element(by=By.XPATH, value=
                "/html/body/div/div/div/div/div[1]/section/div/div/div[2]/div[3]/div[1]/button")
                actions = ActionChains(self.driver)
                actions.move_to_element(button).perform()
                button.click()
                time.sleep(3)
                main_wnd = get_current_wnd(self.driver)
                if is_popup_window(self.driver):
                    switch_to_popup_wnd(self.driver)
                    time.sleep(3)
                    self.driver.find_element(by=By.XPATH, value=
                    '/html/body/div/div/section/div[2]/div/div[5]/button').click()
                    switch_to_wnd(self.driver, main_wnd)
                time.sleep(3)

                result = None
                while not result:
                    try:
                        result = self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[1]").text
                        self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[2]/div/div").click()
                    except Exception:
                        time.sleep(5)
                time.sleep(5)
                new_gold, new_wood, new_food, new_enrg = self.get_resources()
                if float(new_wood) > float(wood):
                    self.db.add_claim(
                        Claim(time.time(), float(new_wood) - float(wood), self.db.get_account(self.account).id))
            elif seconds_to_next_mine <= 300:
                time.sleep(60)
            else:
                self.db.update_account(self.account, next_mining_time=(int(time.time()) + seconds_to_next_mine))
                break
