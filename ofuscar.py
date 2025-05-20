from PIL import Image, ImageOps, ImageFilter
import os

PASTA_ORIGINAIS = "Imagens Originais"
PASTA_SILHUETAS = "Imagens Ofuscadas"

if not os.path.exists(PASTA_SILHUETAS):
    os.makedirs(PASTA_SILHUETAS)

# def acizentar_imagem(caminho_original, caminho_saida, fator=0.1):
#     with Image.open(caminho_original) as img:
#         img_gray = ImageOps.grayscale(img)
#         img_gray = img_gray.point(lambda p: int(p * fator))
#         if img.mode in ("RGBA", "LA"):
#             alpha = img.split()[-1]
#             img_gray = Image.merge("LA", (img_gray, alpha)).convert("RGBA")
#         else:
#             img_gray = img_gray.convert("RGBA")
#         img_gray.save(caminho_saida)
#         print(f"Imagem acinzentada salva: {caminho_saida}")

def obscurecer_imagem(caminho_original, caminho_saida):
    import numpy as np
    import cv2
    from PIL import Image

    with Image.open(caminho_original) as img:
        img = img.convert("RGBA")
        np_img = np.array(img)
        altura, largura = img.size[1], img.size[0]

        # Cria máscara: personagem = 1, fundo branco/transparente = 0
        alpha = np_img[:, :, 3]
        is_not_transparent = alpha > 0
        is_not_white = np.any(np_img[:, :, :3] < 250, axis=2)
        mask = np.logical_and(is_not_transparent, is_not_white).astype(np.uint8) * 255

        # Remove pequenos ruídos (morphological opening)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

        # Encontra todos os contornos externos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            Image.new("RGBA", img.size, (255, 255, 255, 255)).save(caminho_saida)
            print(f"Nenhum contorno encontrado: {caminho_saida}")
            return

        # Seleciona apenas contornos grandes (área > 2% da imagem)
        min_area = (altura * largura) * 0.05
        large_contours = [c for c in contours if cv2.contourArea(c) > min_area]

        # Cria máscara final preenchendo apenas os grandes contornos
        mask_final = np.zeros_like(mask)
        cv2.drawContours(mask_final, large_contours, -1, 255, thickness=cv2.FILLED)

        # Cria imagem de saída: fundo branco, personagem preto
        resultado = np.ones_like(np_img) * 255
        resultado[mask_final == 255] = [0, 0, 0, 255]

        Image.fromarray(resultado).save(caminho_saida)
        print(f"Imagem obscurecida polida salva: {caminho_saida}")

# Percorre todas as subpastas em PASTA_ORIGINAIS
for subdir, dirs, files in os.walk(PASTA_ORIGINAIS):
    for arquivo in files:
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg")) and "_" not in arquivo:
            # Caminho relativo da subpasta
            rel_dir = os.path.relpath(subdir, PASTA_ORIGINAIS)
            # Cria a mesma estrutura de pastas em PASTA_SILHUETAS
            pasta_destino = os.path.join(PASTA_SILHUETAS, rel_dir)
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
            caminho_original = os.path.join(subdir, arquivo)
            caminho_saida = os.path.join(pasta_destino, arquivo.lower())
            obscurecer_imagem(caminho_original, caminho_saida)