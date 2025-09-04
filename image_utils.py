
from PIL import Image
import numpy as np
import cv2

def obscure_image(original_path, output_path):
	"""
	Generates an obscured version of the original image and saves it to the output path.
	The character is black, the background is white.
	"""
	with Image.open(original_path) as img:
		img = img.convert("RGBA")
		np_img = np.array(img)
		height, width = img.size[1], img.size[0]
		is_not_white = np.any(np_img[:, :, :3] < 245, axis=2)
		mask = is_not_white.astype(np.uint8) * 255
		contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if not contours:
			Image.new("RGBA", img.size, (255, 255, 255, 255)).save(output_path)
			return
		min_area = (height * width) * 0.05
		large_contours = [c for c in contours if cv2.contourArea(c) > min_area]
		if not large_contours:
			Image.new("RGBA", img.size, (255, 255, 255, 255)).save(output_path)
			return
		final_mask = np.zeros_like(mask)
		cv2.drawContours(final_mask, large_contours, -1, 255, thickness=cv2.FILLED)
		result = np.ones((height, width, 4), dtype=np.uint8) * 255
		result[final_mask == 255] = [0, 0, 0, 255]
		Image.fromarray(result).save(output_path)
