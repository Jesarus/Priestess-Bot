import json
import os

DB_PATH = "pontuacoes.json"

def carregar_pontuacoes():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_pontuacoes(pontuacoes):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(pontuacoes, f, ensure_ascii=False, indent=2)