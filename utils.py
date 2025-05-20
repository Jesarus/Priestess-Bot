def carregar_nomes_alternativos(caminho="nomes_alternativos.txt"):
    nomes = {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if ";" in linha:
                    chave, valores = linha.strip().split(";", 1)
                    nomes[chave.lower()] = [v.strip().lower() for v in valores.split(",")]
    except FileNotFoundError:
        pass
    return nomes