import requests
import json


class MockClicker:
    def __init__(self, account_name):
        self.account = account_name

    def get_account_resources(self):
        response = requests.get(f"http://172.17.0.2:5000/accounts/{self.account}/resources")
        return json.loads(response.text)

    def get_account_lands(self):
        response = requests.get(f"http://172.17.0.2:5000/accounts/{self.account}/lands")
        return json.loads(response.text)

    def get_land_ph(self, land_name):
        response = requests.get(f"http://172.17.0.2:5000/accounts/{self.account}/{land_name}/ph")
        return json.loads(response.text)

    def get_land_wait_time(self, land_name):
        response = requests.get(f"http://172.17.0.2:5000/accounts/{self.account}/{land_name}/wait_time")
        return json.loads(response.text)

    def get_land_equipments(self, land_name):
        response = requests.get(f"http://172.17.0.2:5000/accounts/{self.account}/{land_name}/equipments")
        return json.loads(response.text)

    def get_land_fee(self, land_name):
        response = requests.get(f"http://172.17.0.2:5000/accounts/{self.account}/{land_name}/fee")
        return json.loads(response.text)

    def claim_land(self, land_name):
        response = requests.post(f"http://172.17.0.2:5000/accounts/{self.account}/{land_name}/claim", data={'pwd':'linuxize'})
        return response.text == "ok"
