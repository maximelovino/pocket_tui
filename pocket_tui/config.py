import os
from pathlib import Path
from dotenv import load_dotenv
from PyInquirer import prompt


KEYS_CONFIG_FILENAME = ".pocket_cli"
KEYS_CONFIG_FILE = os.path.join(Path.home(), KEYS_CONFIG_FILENAME)
POCKET_ENV_NAME = 'POCKET_CONSUMER_KEY'
YOUTUBE_ENV_NAME = 'YOUTUBE_KEY'
class Config():
    def __init__(self):
        if not os.path.isfile(KEYS_CONFIG_FILE):
            self.create_keys_file()

        load_dotenv(KEYS_CONFIG_FILE)
        self.pocket_key = os.getenv(POCKET_ENV_NAME)
        self.youtube_key = os.getenv(YOUTUBE_ENV_NAME)
        if self.youtube_key is None or self.pocket_key is None:
            print(f"Pocket CLI config file incomplete, please delete {KEYS_CONFIG_FILE} file and relaunch the program")

    def create_keys_file(self):
        questions = [
            {
                "type": "input",
                "name": "pocket_consumer_key",
                "message": "Type your Pocket Consumer Key"
            },
            {
                "type": "input",
                "name": "youtube_key",
                "message": "Type your Youtube Data API Key"
            }
        ]

        answers = prompt(questions)
        try:
            file_content = f"{POCKET_ENV_NAME}={answers['pocket_consumer_key']}\n{YOUTUBE_ENV_NAME}={answers['youtube_key']}"

            with open(KEYS_CONFIG_FILE,'w') as f:
                f.write(file_content)
            print("New config file created")
        except:
            print("There was an error, exiting...")
            exit(1)


