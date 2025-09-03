import json

def carregar_nomes_alternativos(caminho="nomes_alternativos.json"):
    """
    Carrega nomes alternativos de operadores a partir de um arquivo JSON.
    O arquivo deve ter o formato: {"NomePrincipal": ["alternativo1", "alternativo2", ...], ...}
    Retorna um dicionário com as chaves e valores em minúsculo para facilitar a busca.
    """
    nomes = {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for chave, lista in dados.items():
                nomes[chave.lower()] = [v.strip().lower() for v in lista]
    except FileNotFoundError:
        pass
    return nomes