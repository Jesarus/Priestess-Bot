import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from scores import load_scores, save_scores, DB_PATH

def test_save_and_load_scores(tmp_path):
    # Use a temporary path to avoid affecting the real database
    test_db = tmp_path / "scores.json"
    data = {"123": {"username": "user", "pontos": 42}}
    # Save
    with open(test_db, "w", encoding="utf-8") as f:
        json.dump(data, f)
    # Load using the project function
    original_db_path = DB_PATH
    try:
        # Temporarily point DB_PATH to the test file
        import scores
        scores.DB_PATH = str(test_db)
        loaded = load_scores()
        assert loaded == data
    finally:
        scores.DB_PATH = original_db_path

def test_save_scores_creates_file(tmp_path):
    data = {"456": {"username": "other", "pontos": 10}}
    # Save using the project function
    save_scores(data)
    assert os.path.exists(DB_PATH)