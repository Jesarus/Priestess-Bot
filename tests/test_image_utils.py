import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_utils import obscure_image
from PIL import Image
import numpy as np

def test_obscure_image(tmp_path):
    # Create a simple image (black in the center, white in the background)
    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    for x in range(3, 7):
        for y in range(3, 7):
            img.putpixel((x, y), (0, 0, 0, 255))
    original = tmp_path / "original.png"
    output = tmp_path / "output.png"
    img.save(original)
    obscure_image(str(original), str(output))
    # Check if the output image exists and has the same size
    assert os.path.exists(output)
    out_img = Image.open(output)
    assert out_img.size == (10, 10)
    arr = np.array(out_img)
    # The center should be black, the rest white
    assert (arr[5,5][:3] == [0,0,0]).all()
    assert (arr[0,0][:3] == [255,255,255]).all()
