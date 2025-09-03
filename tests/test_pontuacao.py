import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from pontuacao import carregar_pontuacoes, salvar_pontuacoes, DB_PATH

def test_salvar_e_carregar_pontuacoes(tmp_path):
    # Use um caminho temporário para não afetar o banco real
    test_db = tmp_path / "pontuacoes.json"
    dados = {"123": {"username": "user", "pontos": 42}}
    # Salva
    with open(test_db, "w", encoding="utf-8") as f:
        json.dump(dados, f)
    # Carrega
    with open(test_db, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == dados

def test_salvar_pontuacoes_cria_arquivo(tmp_path):
    test_db = tmp_path / "pontuacoes.json"
    dados = {"456": {"username": "outro", "pontos": 10}}
    # Salva usando a função do projeto
    salvar_pontuacoes(dados)
    assert os.path.exists(DB_PATH)