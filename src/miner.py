import argparse
import base64
import json
import logging
import time
import os

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from claimer import ClaimXPS
from storage import CredStorage


class Miner:
    def __init__(self, main_cfg, acc_cfg, driver, verbose=False):
        self.main_cfg = main_cfg
        self.acc_cfg = acc_cfg
        self.driver = driver
        self.verbose = verbose
        self.db = CredStorage()

    def reddit_login(self, login, pwd):
        self.driver.get("https://www.reddit.com/login/")
        time.sleep(3)
        ilogin = self.driver.find_element(by=By.XPATH,
                                          value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input')
        ipwd = self.driver.find_element(by=By.XPATH,
                                        value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input')

        ilogin.send_keys(login)
        ipwd.send_keys(pwd)

        lgn_btn = self.driver.find_element(by=By.XPATH,
                                           value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')
        lgn_btn.click()

        time.sleep(5)
        driver.get("https://all-access.wax.io")
        time.sleep(5)
        reddit_login = self.driver.find_element(by=By.XPATH,
                                                value='/html/body/div/div/div/div/div[4]/div[1]/div[9]/button')
        reddit_login.click()
        time.sleep(5)
        try:
            allow_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/form/div/input[1]')
        except Exception:
            ilogin = self.driver.find_element(by=By.XPATH,
                                              value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input')
            ipwd = self.driver.find_element(by=By.XPATH,
                                            value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input')

            ilogin.send_keys(login)
            ipwd.send_keys(pwd)

            lgn_btn = self.driver.find_element(by=By.XPATH,
                                               value='/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')
            lgn_btn.click()

            allow_btn = None
            wait_iterator = 0
            while not allow_btn:
                if wait_iterator > 15:
                    raise Exception
                try:
                    allow_btn = self.driver.find_element(by=By.XPATH,
                                                         value='/html/body/div[3]/div/div[2]/form/div/input[1]')
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

    def mail_login(self, login, pwd):
        driver.get("https://all-access.wax.io")
        time.sleep(3)
        wax_login = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div[5]/div/div/div/div[1]/div[1]/input')
        wax_pass = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div[5]/div/div/div/div[1]/div[2]/input')

        wax_login.send_keys(login)
        wax_pass.send_keys(pwd)

        wax_login_button = self.driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div[5]/div/div/div/div[4]/button')
        time.sleep(1)
        wax_login_button.click()

        time.sleep(10)
        try:
            if self.driver.find_element_by_xpath("/html/body/div/div/section/div[2]/div/div[2]"):
                while not os.path.exists(".mail-login-code"):
                    time.sleep(3)
                mail_code = ''
                while not mail_code:
                    with open('.mail-login-code') as f:
                        mail_code = f.readlines()
                    time.sleep(3)
                input_code_line = self.driver.find_element_by_xpath("/html/body/div/div/section/div[2]/div/div[3]/form/div[1]/div/input")
                input_code_line.send_keys(mail_code)
                self.driver.find_element_by_xpath("/html/body/div/div/section/div[2]/div/div[3]/form/div[3]/button").click()
        except Exception:
            pass
        time.sleep(5)
        while True:
            try:
                self.driver.find_element_by_xpath('/html/body/div/div/section/div[2]/div/div[2]')
            except:
                break
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

    def start(self, acc_name, rent=False):
        def login_with_update_token():
            lg = base64.b64decode(self.acc_cfg[acc_name]["login"]).decode("utf-8")
            pw = base64.b64decode(self.acc_cfg[acc_name]["pass"]).decode("utf-8")

            if self.acc_cfg[acc_name]["auth"] == "reddit":
                logging.info("Login with reddit auth")
                token_id, session_token = self.reddit_login(lg, pw)
            else:
                logging.info("Login with mail auth")
                token_id, session_token = self.mail_login(lg, pw)
            self.db.update_account({"name": acc_name, "session_token": session_token, "session_id": token_id, "token_upd_time": int(time.time())})

        db_account = self.db.get_account(acc_name)
        logging.info(f"DB_ACCOUNT: {db_account}")

        if not db_account:
            logging.info(f"Not {acc_name} in database create it")
            self.db.add_account({"name": acc_name, "session_token": None, "session_id": None, "token_upd_time": int(time.time())})
            db_account = self.db.get_account(acc_name)

        if not db_account['session_token'] or not db_account['session_id']:
            logging.info("Login without token")
            try:
                login_with_update_token()
            except Exception:
                return
        else:
            logging.info("Login with token")
            try:
                self.token_login(token_id=db_account['session_id'], session_token=db_account['session_token'])
            except Exception:
                return

        claimer = ClaimXPS(account=acc_name, config=self.main_cfg, driver=driver, rent=rent)
        while True:
            #if claimer.claim_xps():
            #    claimer.claim_stake()
            claimer.claim_xps()
            time.sleep(60)

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", help="run with X server for debug", action='store_true')
    parser.add_argument("--d", help="run with debug mode", action='store_true')
    parser.add_argument("--v", help="run with verbose mode", action='store_true')
    parser.add_argument("--config", help="config file")
    parser.add_argument("--accounts", help="accounts file")
    parser.add_argument("--rent", help="if need rent claims", action='store_true')
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

    with open(args.accounts) as f:
        acc_cfg = json.load(f)

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        for acc_name in acc_cfg:
            logging.info(f"Start mining for account {acc_name}")
            driver = webdriver.Chrome(options=set_extension)
            WebDriverWait(driver, 5)
            Miner(main_cfg,
                  acc_cfg,
                  driver,
                  verbose=True if args.v else False).start(acc_name, rent=True if args.rent else False)
