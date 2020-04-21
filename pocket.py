from dotenv import load_dotenv
import os
import webbrowser
import requests
import json
from entry import Entry
from typing import List


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
        # print(f"Authenticated with key {self.key} and token {self.token}")

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

    def retrieve_full_list(self) -> List[Entry]:
        get_url = f"{BASE_POCKET_URL}get"
        get_payload = {"consumer_key": self.key,
                       "access_token": self.token, "sort": "newest"}
        get_request = requests.get(
            get_url, data=json.dumps(get_payload), headers=BASE_HEADERS)
        response = get_request.json()
        dictionnary = response['list']
        entries = Entry.parse_list(dictionnary.values())
        return entries
    
    def archive(self, entry: Entry):
        actions = [{"action": "archive", "item_id": entry.id}]
        self.send_actions(actions)

    def bulk_delete(self, entries: List[Entry]):
        actions = [{'action': 'delete', "item_id": entry.id} for entry in entries]
        self.send_actions(actions)

    def send_actions(self, actions: List):
        send_url = f"{BASE_POCKET_URL}send"
        payload = {"consumer_key": self.key, "access_token": self.token,
                   "actions": actions}
        request = requests.get(
            send_url, data=json.dumps(payload), headers=BASE_HEADERS)
        print(request.json())
