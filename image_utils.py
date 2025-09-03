
from PIL import Image
import numpy as np
import cv2

def obscurecer_imagem(caminho_original, caminho_saida):
	"""
	Gera uma versão obscurecida da imagem original e salva no caminho de saída.
	O personagem fica preto, o fundo branco.
	"""
	with Image.open(caminho_original) as img:
		img = img.convert("RGBA")
		np_img = np.array(img)
		altura, largura = img.size[1], img.size[0]
		is_not_white = np.any(np_img[:, :, :3] < 245, axis=2)
		mask = is_not_white.astype(np.uint8) * 255
		contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if not contours:
			Image.new("RGBA", img.size, (255, 255, 255, 255)).save(caminho_saida)
			return
		min_area = (altura * largura) * 0.05
		large_contours = [c for c in contours if cv2.contourArea(c) > min_area]
		if not large_contours:
			Image.new("RGBA", img.size, (255, 255, 255, 255)).save(caminho_saida)
			return
		mask_final = np.zeros_like(mask)
		cv2.drawContours(mask_final, large_contours, -1, 255, thickness=cv2.FILLED)
		resultado = np.ones((altura, largura, 4), dtype=np.uint8) * 255
		resultado[mask_final == 255] = [0, 0, 0, 255]
		Image.fromarray(resultado).save(caminho_saida)
