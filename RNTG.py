from random import randint

from PIL import Image
import numpy as np


class Noise:

    TILE_WIDTH = 150
    TILE_HEIGHT = 150
    # set density to 1..80000
    DENSITY = 25000
    IMG_RESOLUTION = 1000

    def __init__(self):
        self.disp = [[0 for x in range(self. TILE_WIDTH)] for x in range(self.TILE_HEIGHT)]
        self.minim = 0
        self.maxim = 0
        self.dif = 0

    def set_zero(self):
        self.disp = [[0 for x in range(self.TILE_WIDTH)] for x in range(self.TILE_HEIGHT)]

    def print_array(self):
        for i in range(len(self.disp)):
            print(''.join(str(self.disp[i])))

    def born(self):
        x = randint(0, self.TILE_WIDTH - 1)
        y = randint(0, self.TILE_HEIGHT - 1)
        if self.disp[x][y] < 256:
            self.disp[x][y] += 1

    def start(self):
        self.set_zero()
        self.noise(self.DENSITY)
        self.convert()

    def turn(self):
        if any(self.disp[i][j] == 0 for i in range(self.TILE_WIDTH) for j in range(self.TILE_HEIGHT)):
            self.born()

    def noise(self, seed):
        seed = seed % 100000
        for i in range(seed):
            self.turn()
        return self.disp

    def minimum(self):
        self.minim = min([self.disp[i][j] for i in range(self.TILE_WIDTH) for j in range(self.TILE_HEIGHT)])
        return self.minim

    def maximum(self):
        self.maxim = max([self.disp[i][j] for i in range(self.TILE_WIDTH) for j in range(self.TILE_HEIGHT)])
        return self.maxim

    def push(self, n):
        # if using m instead of self.dif tiles have different density
        # m = self.maxim - self.minim
        return abs((n - self.minim)*255//self.dif) if self.dif != 0 else 255

    def convert(self):
        self.minimum()
        self.maximum()
        for i in range(self.TILE_WIDTH):
            for j in range(self.TILE_HEIGHT):
                self.disp[i][j] = self.push(self.disp[i][j])

    def tile(self):
        self.convert()
        array = np.array(self.disp, dtype=np.uint8)
        image = Image.fromarray(array)
        return image

    def noise_texture(self):
        x = self.IMG_RESOLUTION // self.TILE_WIDTH
        y = self.IMG_RESOLUTION // self.TILE_HEIGHT

        self.noise(self.DENSITY)
        self.dif = self.maximum() - self.minimum()

        texture = Image.new('RGB', (self.TILE_WIDTH * x, self.TILE_HEIGHT * y))
        for i in range(x):
            for j in range(y):
                self.start()
                print('We are at tile #{}/{}'.format(i*x + j + 1, x * y))
                texture.paste(self.tile(), (self.TILE_WIDTH*i, self.TILE_HEIGHT*j))
        texture.save('noise_texture.png')
        texture.show()


a = Noise()
a.noise_texture()
