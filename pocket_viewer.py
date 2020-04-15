import requests
import json
import os
import webbrowser
from dotenv import load_dotenv
from PyInquirer import prompt
import time
from pocket import Pocket




def play_entry(entry, pocket_client):
    identifier = entry['id']
    title = entry['name']
    url = entry['url']
    print(identifier)
    print(title)
    print(url)
    os.system(f"mpv {url}")
    to_delete = input("Do you want to archive the entry?[y/N]")
    if to_delete == 'y':
        pocket_client.archive(identifier)
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


pocket_client = Pocket()


while True:
    normal_domain_list = pocket_client.retrieve_list("youtube.com", 100)
    short_domain_list = pocket_client.retrieve_list("youtu.be", 100)

    joined_list = normal_domain_list + short_domain_list

    sorted_list = sorted(
        joined_list, key=lambda x: x["time_updated"], reverse=True)

    video = choose_video(sorted_list[:100])
    print(video)
    play_entry(video, pocket_client)
