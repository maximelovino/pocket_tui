from dotenv import load_dotenv
import os
import webbrowser
import requests
import json


BASE_POCKET_URL = "https://getpocket.com/v3/"
BASE_HEADERS = {"Content-Type": "application/json",
                "X-Accept": "application/json"}

TOKEN_CACHE_FILE = ".token"


class Pocket():
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.key = os.getenv('POCKET_CONSUMER_KEY')
        self.token = self.cached_authentication()
        print(f"Authenticated with key {self.key} and token {self.token}")

    def cached_authentication(self) -> str:
        if os.path.exists(TOKEN_CACHE_FILE):
            print("Using cache for authentication")
            with open(TOKEN_CACHE_FILE, 'r') as f:
                token = f.read()
                return token
        else:
            print("Need to authenticate")
            token = self.authenticate()
            with open(TOKEN_CACHE_FILE, 'w') as f:
                f.write(token)
            return token

    def authenticate(self) -> str:
        request_url = f"{BASE_POCKET_URL}oauth/request"
        redirect_uri = "http://www.google.com"
        payload = {"consumer_key": self.key, "redirect_uri": redirect_uri}

        request = requests.post(request_url, headers=BASE_HEADERS,
                                data=json.dumps(payload))
        code = request.json()['code']

        webbrowser.open(
            f'https://getpocket.com/auth/authorize?request_token={code}&redirect_uri={redirect_uri}')

        input("Press Enter to continue...")
        access_token_url = f"{BASE_POCKET_URL}oauth/authorize"
        payload = {"consumer_key": self.key, "code": code}

        access_token_request = requests.post(
            access_token_url, headers=BASE_HEADERS, data=json.dumps(payload))

        access_token = access_token_request.json()['access_token']
        return access_token

    def retrieve_list(self, domain: str, count: int):
        get_url = f"{BASE_POCKET_URL}get"
        get_payload = {"consumer_key": self.key,
                       "access_token": self.token, "domain": domain, "count": count, "sort": "newest"}
        get_request = requests.get(
            get_url, data=json.dumps(get_payload), headers=BASE_HEADERS)
        response = get_request.json()
        dictionnary = response['list']
        return list(dictionnary.values())

    def archive(self, item_id):
        print(f"Archiving {item_id}")
        archive_url = f"{BASE_POCKET_URL}send"
        payload = {"consumer_key": self.key, "access_token": self.token,
                   "actions": [{"action": "archive", "item_id": item_id}]}
        request = requests.get(
            archive_url, data=json.dumps(payload), headers=BASE_HEADERS)
        print(request.json())
