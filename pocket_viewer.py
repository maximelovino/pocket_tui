import requests
import json
import os
import webbrowser
from dotenv import load_dotenv
from PyInquirer import prompt
import time
from pocket import Pocket
from typing import List, Dict, Tuple
from entry import Entry, VideoEntry, ArticleEntry


def choose_video(xs: List[VideoEntry]) -> VideoEntry:
    questions = [
        {
            'type': 'list',
            'name': 'video_choice',
            'message': 'What do you want to play?',
            'choices': [
                {'name': x.list_str(), 'value': x} for x in xs]
        }
    ]
    answers = prompt(questions)
    return answers['video_choice']


def watch_youtube(videos: List[VideoEntry], pocket_client: Pocket):
    chosen = choose_video(videos)
    print(chosen)
    chosen.open()
    # TODO replace with inquirer confirm
    to_delete = input("Do you want to archive the entry?[y/N]")
    if to_delete == 'y':
        pocket_client.archive(chosen)


def group_by_year(entries: List[Entry]) -> Dict[str, List[Entry]]:
    dict_by_year = {}
    for entry in entries:
        year = str(entry.updated.year)
        if year not in dict_by_year:
            dict_by_year[year] = []
        dict_by_year[year].append(entry)
    return dict_by_year


def filter_youtube(entries: List[Entry]) -> List[Entry]:
    return list(filter(lambda x: isinstance(x, VideoEntry), entries))


def refresh(pocket_client: Pocket) -> Tuple[List[Entry], Dict[str, List[Entry]], List[VideoEntry]]:
    full_list = pocket_client.retrieve_full_list()
    by_year = group_by_year(full_list)
    youtube_list = filter_youtube(full_list)
    return full_list, by_year, youtube_list


# TODO replace str by an enum
def main_menu() -> str:
    questions = [
        {
            'type': 'list',
            'name': 'menu_choice',
            'message': 'What do you want to do?',
            'choices': [
                {'name': "Watch YouTube videos", 'value': 'youtube'},
                {'name': "Bulk operations", 'value': 'bulk'},
                {'name': "Bulk-delete by year", 'value': 'delete_year'},
                {'name': "Refresh", 'value': 'refresh'},
                {'name': "Quit", 'value': 'quit'}
            ]
        }
    ]
    answers = prompt(questions)
    return answers['menu_choice']


def delete_by_year(by_year: Dict[str, List[Entry]]) -> None:
    questions = [
        {
            'type': 'list',
            'name': 'year_to_delete',
            'message': 'What year do you want to bulk-delete?',
            'choices': [
                    {'name': f"{key} - {len(by_year[key])} entries", 'value': key} for key in by_year.keys()
            ]
        },
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Confirm bulk-deletion?'
        }
    ]
    answers = prompt(questions)
    if answers['confirm']:
        year = answers['year_to_delete']
        print(f"Bulk-deleting entries from {year}")
        pocket_client.bulk_delete(by_year[year])
    else:
        print("Deletion NOT confirmed")


def bulk_operations(entries: List[Entry]) -> None:
    questions = [
        {
            'type': 'checkbox',
            'name': 'chosen_entries',
            'message': 'Select entries',
            'choices': [
                {'name': x.list_str(), 'value': x} for x in entries]
        },
        {
            'type': 'list',
            'name': 'operation',
            'message': 'Select operation',
            'choices': [
                {'name': "Open", 'value': "open"},
                {'name': "Archive", 'value': "archive"},
                {'name': "Delete", 'value': "delete"},
            ]
        },
    ]
    answers = prompt(questions)
    print(answers)
    if answers["operation"] == "open":
        chosen = answers['chosen_entries']
        for x in chosen:
            x.open()



running = True

pocket_client = Pocket()
full_list, by_year, youtube_list = refresh(pocket_client)

while running:
    menu_choice = main_menu()
    if menu_choice == 'refresh':
        full_list, by_year, youtube_list = refresh(pocket_client)
    elif menu_choice == 'quit':
        print("Quitting")
        exit(0)
    elif menu_choice == 'delete_year':
        delete_by_year(by_year)
    elif menu_choice == 'youtube':
        watch_youtube(youtube_list, pocket_client)
    elif menu_choice == 'bulk':
        bulk_operations(full_list)
    else:
        print("You broke the menu")
