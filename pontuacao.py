import os
from config import PONTUACOES_PATH

def carregar_pontuacoes():
    pontuacoes = {}
    if os.path.exists(PONTUACOES_PATH):
        with open(PONTUACOES_PATH, "r", encoding="utf-8") as f:
            for linha in f:
                user_id, username, pontos = linha.strip().split(";", 2)
                pontuacoes[user_id] = {"username": username, "pontos": int(pontos)}
    return pontuacoes

def salvar_pontuacoes(pontuacoes):
    with open(PONTUACOES_PATH, "w", encoding="utf-8") as f:
        for user_id, dados in pontuacoes.items():
            f.write(f"{user_id};{dados['username']};{dados['pontos']}\n")