import requests
import json
import os
import webbrowser
from dotenv import load_dotenv
from PyInquirer import prompt
import time
from pocket import Pocket
from typing import List, Dict, Tuple, Callable, Union
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


def watch_youtube(videos: List[VideoEntry], pocket_client: Pocket) -> None:
    chosen = choose_video(videos)
    print(chosen)
    chosen.open()
    # TODO replace with inquirer confirm
    to_delete = input("Do you want to archive the entry?[y/N]")
    if to_delete == 'y':
        pocket_client.archive([chosen])


def youtube(all_entries: List[Entry], filter_func: Callable[[List[Entry]], Union[List[Entry], Dict[str, List[Entry]]]], client: Pocket) -> None:
    yt_list = filter_youtube(all_entries)
    filtered = apply_filter(yt_list, filter_func)
    if len(filtered) == 0:
        return
    watch_youtube(filtered, pocket_client)


def filter_youtube(entries: List[Entry]) -> List[VideoEntry]:
    return list(filter(lambda x: isinstance(x, VideoEntry), entries))


def refresh(client: Pocket) -> List[Entry]:
    full_list = pocket_client.retrieve_full_list()
    return full_list


def filter_question_needed(answers):
    return answers["menu_choice"] == youtube or answers["menu_choice"] == bulk_operations


def no_filter(entries: List[Entry]) -> List[Entry]:
    return entries


def search_filter(entries: List[Entry]) -> List[Entry]:
    questions = [
        {
            "type": "input",
            "name": "query",
            "message": "Type your query"
        }]
    answers = prompt(questions)
    query = answers["query"]
    return list(filter(lambda x: query in str(x).lower(), entries))


def group_by_year(entries: List[Entry]) -> Dict[str, List[Entry]]:
    return group_by(entries, lambda entry: str(entry.updated.year))


def group_by_year_month(entries: List[Entry]) -> Dict[str, List[Entry]]:
    return group_by(entries, lambda entry: f"{entry.updated.year} / {entry.updated.month}")


def group_by_domain_channel(entries: List[Entry]) -> Dict[str, List[Entry]]:
    return group_by(entries, lambda x: x.domain_filter())


def group_by(entries: List[Entry], key_function: Callable[[Entry], str]) -> Dict[str, List[Entry]]:
    dict_by = {}
    for entry in entries:
        key = key_function(entry)
        if key not in dict_by:
            dict_by[key] = []
        dict_by[key].append(entry)
    return dict_by


def main_menu() -> str:
    questions = [
        {
            'type': 'list',
            'name': 'menu_choice',
            'message': 'What do you want to do?',
            'choices': [
                {'name': "Watch YouTube videos", 'value': youtube},
                {'name': "Bulk operations", 'value': bulk_operations},
                {'name': "Quit", 'value': quit}
            ]
        },
        {
            'type': 'list',
            'name': 'filter_choice',
            'message': 'What kind of filtering do you want?',
            'when': filter_question_needed,
            'choices': [
                {'name': "No filter", 'value': no_filter},
                {'name': "Group by year", 'value': group_by_year},
                {'name': "Group by year/month", 'value': group_by_year_month},
                {'name': "Group by domain/channel",
                    'value': group_by_domain_channel},
                {'name': "Search", 'value': search_filter},
            ]
        },
    ]
    answers = prompt(questions)
    return answers


def select_from_dict(dictionnary: Dict[str, List[Entry]]) -> List[Entry]:
    questions = [{
        'type': 'list',
        'name': 'key',
        'message': 'Select key',
        'choices': dictionnary.keys()
    }]
    answers = prompt(questions)
    return dictionnary[answers['key']]


def apply_filter(all_entries: List[Entry], filter_func: Callable[[List[Entry]], Union[List[Entry], Dict[str, List[Entry]]]]) -> List[Entry]:
    filtered = filter_func(all_entries)

    if isinstance(filtered, dict):
        return select_from_dict(filtered)
    else:
        return filtered


def bulk_operations(all_entries: List[Entry], filter_func: Callable[[List[Entry]], Union[List[Entry], Dict[str, List[Entry]]]], client: Pocket) -> None:
    entries = apply_filter(all_entries, filter_func)

    if len(entries) == 0:
        return
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
    chosen = answers['chosen_entries']
    if answers["operation"] == "open":
        for x in chosen:
            x.open()
        questions = [
            {
                'type': 'confirm',
                'name': 'confirm',
                'message': 'Do you want to archive as well?'
            }
        ]
        confirm = prompt(questions)
        if confirm["confirm"]:
            client.archive(chosen)
    else:
        questions = [
            {
                'type': 'confirm',
                'name': 'confirm',
                'message': 'Confirm bulk operation?'
            }
        ]
        confirm = prompt(questions)
        if confirm["confirm"]:
            if answers["operation"] == "archive":
                client.archive(chosen)
            elif answers["operation"] == "delete":
                client.delete(chosen)


running = True

pocket_client = Pocket()

while running:
    full_list = refresh(pocket_client)
    menu_choice = main_menu()
    menu_choice['menu_choice'](
        full_list, menu_choice['filter_choice'], pocket_client)


def quit(xs: List[Entry], filter_func: Callable[[List[Entry]], Union[List[Entry], Dict[str, List[Entry]]]], client: Pocket) -> None:
    exit(0)  # TODO not classy
