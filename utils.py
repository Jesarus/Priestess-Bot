import json

def load_alternative_names(path="alternative_names.json"):
    """
    Loads alternative operator names from a JSON file.
    The file must have the format: {"MainName": ["alternative1", "alternative2", ...], ...}
    Returns a dictionary with keys and values in lowercase for easier search.
    """
    names = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key, lst in data.items():
                names[key.lower()] = [v.strip().lower() for v in lst]
    except FileNotFoundError:
        pass
    return names