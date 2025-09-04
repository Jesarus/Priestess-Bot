import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import load_alternative_names

def test_load_alternative_names(tmp_path):
    # Create a temporary alternative names JSON file
    file = tmp_path / "alternative_names.json"
    data = {
        "Amiya": ["Amiya", "Amiya Caster"],
        "Ch'en": ["Ch'en", "Ch'en the Holungday"]
    }
    file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    names = load_alternative_names(str(file))
    assert "amiya" in names
    assert "ch'en" in names
    assert "amiya caster" in names["amiya"]
    assert "ch'en the holungday" in names["ch'en"]
