import os
import json
import scores

def test_save_and_load_scores(tmp_path):
    # Use a temporary path to avoid affecting the real database
    test_db = tmp_path / "scores.json"
    data = {"123": {"username": "user", "pontos": 42}}
    # Save
    with open(test_db, "w", encoding="utf-8") as f:
        json.dump(data, f)
    # Load using the project function
    original_db_path = scores.DB_PATH
    try:
        # Temporarily point DB_PATH to the test file
        scores.DB_PATH = str(test_db)
        loaded = scores.load_scores()
        assert loaded == data
    finally:
        scores.DB_PATH = original_db_path


def test_save_scores_creates_file(tmp_path):
    data = {"456": {"username": "other", "pontos": 10}}
    test_db = tmp_path / "scores.json"
    original_db_path = scores.DB_PATH
    try:
        scores.DB_PATH = str(test_db)
        scores.save_scores(data)
        assert os.path.exists(test_db)
    finally:
        scores.DB_PATH = original_db_path
