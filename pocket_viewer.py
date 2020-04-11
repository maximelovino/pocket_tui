import requests
import json
import os
import webbrowser
from dotenv import load_dotenv
from PyInquirer import prompt
import time


load_dotenv()

POCKET_KEY = os.getenv('POCKET_CONSUMER_KEY')
print(POCKET_KEY)
BASE_POCKET_URL = "https://getpocket.com/v3/"
headers = {"Content-Type": "application/json", "X-Accept": "application/json"}


def authenticate() -> str:
    request_url = f"{BASE_POCKET_URL}oauth/request"
    redirect_uri = "http://www.google.com"
    payload = {"consumer_key": POCKET_KEY, "redirect_uri": redirect_uri}

    request = requests.post(request_url, headers=headers,
                            data=json.dumps(payload))
    code = request.json()['code']

    webbrowser.open(
        f'https://getpocket.com/auth/authorize?request_token={code}&redirect_uri={redirect_uri}')

    input("Press Enter to continue...")
    access_token_url = f"{BASE_POCKET_URL}oauth/authorize"
    payload = {"consumer_key": POCKET_KEY, "code": code}

    access_token_request = requests.post(
        access_token_url, headers=headers, data=json.dumps(payload))

    access_token = access_token_request.json()['access_token']
    return access_token


TOKEN = authenticate()


def retrieve_list(domain: str, count: int, token: str):
    get_url = f"{BASE_POCKET_URL}get"
    get_payload = {"consumer_key": POCKET_KEY,
                   "access_token": token, "domain": domain, "count": count, "sort": "newest"}
    get_request = requests.get(
        get_url, data=json.dumps(get_payload), headers=headers)
    response = get_request.json()
    dictionnary = response['list']
    return list(dictionnary.values())


def play_entry(entry, token):
    identifier = entry['id']
    title = entry['name']
    url = entry['url']
    print(identifier)
    print(title)
    print(url)
    os.system(f"mpv {url}")
    to_delete = input("Do you want to archive the entry?[y/N]")
    if to_delete == 'y':
        archive(identifier, token)
    print("==========")


def choose_video(xs):
    questions = [
        {
            'type': 'list',
            'name': 'video_choice',
            'message': 'What do you want to play?',
            'choices': [
                {'name': x['resolved_title'], 'value': {'name': x['resolved_title'], 'id': x['item_id'], 'url':x['resolved_url']}} for x in xs]
        }
    ]
    answers = prompt(questions)
    return answers['video_choice']


def archive(item_id, token):
    print(f"Archiving {item_id}")
    archive_url = f"{BASE_POCKET_URL}send"
    payload = {"consumer_key": POCKET_KEY, "access_token": token,
               "actions": [{"action": "archive", "item_id": item_id}]}
    request = requests.get(
        archive_url, data=json.dumps(payload), headers=headers)
    print(request.json())


while True:
    normal_domain_list = retrieve_list("youtube.com", 100, TOKEN)
    short_domain_list = retrieve_list("youtu.be", 100, TOKEN)

    joined_list = normal_domain_list + short_domain_list

    sorted_list = sorted(
        joined_list, key=lambda x: x["time_updated"], reverse=True)

    video = choose_video(sorted_list[:100])
    print(video)
    play_entry(video, TOKEN)
