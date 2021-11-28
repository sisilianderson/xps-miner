import argparse
import base64
import json
import logging
import os
import time
from datetime import datetime

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from database import Storage, Account
from claimer import ClaimXPS


class Miner:
    def __init__(self, main_cfg, acc_cfg, driver, verbose=False):
        self.main_cfg = main_cfg
        self.acc_cfg = acc_cfg
        self.driver = driver
        self.verbose = verbose

    def reddit_login(self, login, pwd):
        self.driver.get("https://www.reddit.com/login/")
        time.sleep(3)
        ilogin = self.driver.find_element(by=By.XPATH, value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input')
        ipwd = self.driver.find_element(by=By.XPATH, value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input')

        ilogin.send_keys(login)
        ipwd.send_keys(pwd)

        lgn_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')
        lgn_btn.click()

        time.sleep(5)
        driver.get("https://all-access.wax.io")
        time.sleep(5)
        reddit_login = self.driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[4]/div[1]/div[9]/button')
        reddit_login.click()
        time.sleep(5)
        try:
            allow_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/form/div/input[1]')
        except Exception:
            ilogin = self.driver.find_element(by=By.XPATH, value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input')
            ipwd = self.driver.find_element(by=By.XPATH, value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input')

            ilogin.send_keys(login)
            ipwd.send_keys(pwd)

            lgn_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')
            lgn_btn.click()

            allow_btn = None
            wait_iterator = 0
            while not allow_btn:
                if wait_iterator > 15:
                    raise Exception
                try:
                    allow_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/form/div/input[1]')
                except Exception:
                    time.sleep(1)
                wait_iterator += 1

        allow_btn.click()

        time.sleep(5)

        token_id = None
        session_token = None
        for cookie in driver.get_cookies():
            if "wax.io" in cookie['domain'] and cookie['name'] == 'AWSALB':
                token_id = cookie['value']
            if "wax.io" in cookie['domain'] and cookie['name'] == 'session_token':
                session_token = cookie['value']
        return token_id, session_token

    def token_login(self, token_id, session_token):
        # Login
        cookies = [
            {
                "name": "token_id",
                "value": token_id,
                "domain": "all-access.wax.io",
                "path": "/"
            }, {
                "name": "session_token",
                "value": session_token,
                "domain": ".wax.io",
                "path": "/"
            }]
        self.driver.get(self.main_cfg["loginPath"])
        for cookie in cookies:
            self.driver.delete_cookie(cookie['name'])
            self.driver.add_cookie(cookie)
        self.driver.get(self.main_cfg["loginPath"])
        time.sleep(15)

    def start(self, acc_name, claim=True):
        def login_with_update_token():
            lg = base64.b64decode(self.acc_cfg[acc_name]["login"]).decode("utf-8")
            pw = base64.b64decode(self.acc_cfg[acc_name]["pass"]).decode("utf-8")

            token_id, session_token = self.reddit_login(lg, pw)
            logging.info(f"token_id: {token_id}\nsession_token: {session_token}")
            db.update_account(acc_name, session_token=session_token, session_id=token_id, token_upd_time=int(time.time()))

        claimer = ClaimXPS(account=acc_name, config=self.main_cfg, driver=driver, db=db)

        if not db.get_account(acc_name).session_token or not db.get_account(acc_name).session_id:
            try:
                pass
                #login_with_update_token()
            except Exception:
                return
        else:
            if (int(time.time()) - db.get_account(acc_name).token_upd_time) > 259200:
                pass
                #login_with_update_token()
            else:
                try:
                    pass
                    #self.token_login(token_id=db.get_account(acc_name).session_id, session_token=db.get_account(acc_name).session_token)
                except Exception:
                    return

        claimer.claim_xps()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", help="run with X server for debug", action='store_true')
    parser.add_argument("--d", help="run with debug mode", action='store_true')
    parser.add_argument("--v", help="run with verbose mode", action='store_true')
    parser.add_argument("--config", help="config file")
    parser.add_argument("--accounts", help="accounts file")
    args = parser.parse_args()
    set_extension = Options()
    if "/" in args.accounts:
        cfg_name = args.accounts.split("/")[-1].replace(".json", "")
    else:
        cfg_name = args.accounts.replace(".json", "")

    if not args.x:
        display = Display(visible=0, size=(900, 900))
        display.start()
        set_extension.add_argument("--no-sandbox")
        set_extension.add_argument("--disable-dev-shm-usage")
    else:
        set_extension.add_argument("--window-size=900,900")

    with open(args.config) as f:
        main_cfg = json.load(f)

    db = Storage(main_cfg["balance_path"], "xps.io")

    with open(args.accounts) as f:
        acc_cfg = json.load(f)

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        for acc_name in acc_cfg:
            if not db.get_account(acc_name):
                logging.info(f"New account {acc_name} found. Create it in the database.")
                db.add_account(Account(name=acc_name, next_mining_time=0))
            if db.get_account(acc_name).next_mining_time < 10 or args.d:
                logging.info(f"Start mining for account {acc_name}")
                driver = webdriver.Chrome(options=set_extension)
                WebDriverWait(driver, 5)
                Miner(main_cfg,
                      acc_cfg,
                      driver,
                      verbose=True if args.v else False).start(acc_name, claim=False if not args.d else True)
                driver.close()
                driver.quit()
            else:
                logging.info(f"The next mining for {acc_name}: {db.get_account(acc_name).next_mining_time} sec")
                time.sleep(30)