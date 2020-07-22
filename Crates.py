import random
from parameters import display


class Crate:
    def __init__(self, height, image, location_x):
        self.location_x = location_x
        self.height = height
        self.image = image

    def draw(self):
        display.blit(self.image, (self.location_x, (self.height)))

