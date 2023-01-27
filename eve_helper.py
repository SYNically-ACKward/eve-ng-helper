# helper.py - basic Eve helper class that includes functions
# to facilitate login, logout, and issue REST GET/POST/DELETE/PUT calls over
# a session

import requests
from datetime import datetime

class eve:
    def __init__(self, url, user, password):
        self.url = "https://" + url + "/api"
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.headers = {'Content-type': 'application/json'}
        requests.packages.urllib3.disable_warnings()


    def login(self, suppression=False):
        try:
            r = self.post("/auth/login", data={"username": self.user,
                          "password": self.password})
            if r.status_code == 200 and suppression == False:
                print(f"{self.url}: Login Success")
                return True
            elif r.status_code == 200 and suppression == True:
                return True
            else:
                print(f"{self.url}: Login Failed: {r.text}")
        except Exception as inst:
            print(f"{self.url}: Exception - unable to connect.")
            print(type(inst))
            print(inst.args)
            print(inst)
            return False


    def post(self, url, data):
        return self.session.post(self.url + url, json=data,
                                 verify=False, timeout=120,
                                 headers=self.headers)


    def get(self, url, payload=None):
        return self.session.get(self.url + url, verify=False,
                                timeout=120, headers=self.headers,
                                data=payload)


    def delete(self, url):
        return self.session.delete(self.url + url,
                                   verify=False, timeout=120,
                                   headers=self.headers)


    def put(self, url, data):
        return self.session.put(self.url + url,
                                json=data, verify=False,
                                timeout=120, headers=self.headers)


    def get_users(self, payload=None):
        return self.session.get(self.url + "/users/", verify=False,
                                timeout=120, headers=self.headers,
                                data=payload)

    def get_user(self, user, payload=None):
        return self.session.get(
            self.url + "/users/" + user, verify=False,
            timeout=120, headers=self.headers, data=payload)

    def create_user(self, data):
        return self.session.post(self.url + "/users", json=data,
                                 verify=False, timeout=120,
                                 headers=self.headers)

    def delete_user(self, user):
        return self.session.delete(self.url + "/users/" + user,
                                   verify=False, timeout=120,
                                   headers=self.headers)

    def update_user(self, user, data):
        return self.session.put(self.url + "/users/" + user,
                                json=data, verify=False, timeout=120,
                                headers=self.headers)

    def running_lab_users(self, payload=None):
        result = self.session.get(self.url + "/runninglabs", verify=False,
        timeout=120, headers=self.headers, data=payload)
        running_lab_users = []
        for lab in result.json().get('data'):
            if lab.get('cpu') != 0 or lab.get('mem') != 0:
                running_lab_users.append(lab.get('username').split("@")[0])
        return set(running_lab_users)


    def running_labs(self, payload=None) -> set:
        result = self.session.get(self.url + "/runninglabs", verify=False,
        timeout=120, headers=self.headers, data=payload)
        running_labs = []
        for lab in result.json().get('data'):
            if lab.get('cpu') != 0 or lab.get('mem') != 0:
                running_labs.append(lab.get('labname'))
        return set(running_labs)


    def logout(self, suppression=False):
        try:
            r = self.get("/auth/logout")
            if r.status_code == 200 and suppression == False:
                print(f"{self.url}: Logout success")
            elif r.status_code == 200 and suppression == True:
                pass
            else:
                print(f"{self.url}: Logout failed: {r.text}")
        except: # noqa
            print(f"{self.url}: Exception - unable to logout")
