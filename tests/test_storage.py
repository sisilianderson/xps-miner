import time

from clicker import MockClicker
from mongodb import Land, Account, PklStorage

accounts = ["ogfv.wam"]

db = PklStorage()


def test_account():
    def get_lands_info():
        res = {}
        for land in clicker.get_account_lands():
            res[land] = {}
            res[land].update(clicker.get_land_ph(land))
            res[land].update({'next_work_wait_time': clicker.get_land_wait_time(land)})
            res[land].update(clicker.get_land_equipments(land))
            res[land].update({'fee': clicker.get_land_fee(land)})
        return res

    while True:
        for account in accounts:
            clicker = MockClicker(account)

            account_res = clicker.get_account_resources()
            account_lands = get_lands_info()
            if not db.get_account(account):
                a = {'name': account}
                a.update(account_res)
                a.update({"lands": account_lands})
                db.add_account(a)

            for acc in db.get_all():
                print("Account info before claim:")
                print(acc)

            for land in account_lands:
                if account_lands[land]['next_work_wait_time'] == 0:
                    clicker.claim_land(land)

            account_res = clicker.get_account_resources()
            account_lands = get_lands_info()
            a = {'name': account}
            a.update(account_res)
            a.update({"lands": account_lands})
            db.update_account(a)

        for acc in db.get_all():
            print("Account info after claim:")
            print(acc)

        time.sleep(60)
