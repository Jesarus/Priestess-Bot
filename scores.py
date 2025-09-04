import json
import os

DB_PATH = "scores.json"

def load_scores():
    """
    Loads the scores from the JSON file. Returns an empty dict if the file does not exist.
    """
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_scores(scores):
    """
    Saves the scores dictionary to the JSON file.
    """
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)