import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import carregar_nomes_alternativos

def test_carregar_nomes_alternativos(tmp_path):
    # Cria um arquivo temporário de nomes alternativos em JSON
    arquivo = tmp_path / "nomes_alternativos.json"
    dados = {
        "Amiya": ["Amiya", "Amiya Caster"],
        "Ch'en": ["Ch'en", "Ch'en the Holungday"]
    }
    arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    nomes = carregar_nomes_alternativos(str(arquivo))
    assert "amiya" in nomes
    assert "ch'en" in nomes
    assert "amiya caster" in nomes["amiya"]
    assert "ch'en the holungday" in nomes["ch'en"]
