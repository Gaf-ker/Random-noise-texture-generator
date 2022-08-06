from PIL import Image
from random import randint
import numpy as np
WIDTH = 1000
HEIGHT = 1000

a = []

for i in range(HEIGHT):
    b = [randint(0, 255) for j in range(WIDTH)]
    a.append(b)

a = np.array(a, dtype=np.uint8)

img = Image.fromarray(a)
img.save('simple_noise.png')
img.show()
