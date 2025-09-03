import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_utils import obscurecer_imagem
from PIL import Image
import numpy as np

def test_obscurecer_imagem(tmp_path):
    # Cria uma imagem simples (preto no centro, branco no fundo)
    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    for x in range(3, 7):
        for y in range(3, 7):
            img.putpixel((x, y), (0, 0, 0, 255))
    original = tmp_path / "original.png"
    saida = tmp_path / "saida.png"
    img.save(original)
    obscurecer_imagem(str(original), str(saida))
    # Verifica se a imagem de saída existe e tem o mesmo tamanho
    assert os.path.exists(saida)
    out_img = Image.open(saida)
    assert out_img.size == (10, 10)
    arr = np.array(out_img)
    # O centro deve ser preto, o resto branco
    assert (arr[5,5][:3] == [0,0,0]).all()
    assert (arr[0,0][:3] == [255,255,255]).all()
