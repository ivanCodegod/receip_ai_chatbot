import os
import json


def load_intents_file():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(
        parent_dir,
        "intents_2024-03-15T13-19-37.json"  # name of the intents data file should be passed here
    )
    with open(path) as file:
        data = json.load(file)

    return data
