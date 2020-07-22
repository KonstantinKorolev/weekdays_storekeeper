from Crates import *


class Insects:
    def __init__(self, image, location_x, location_y):
        self.image = image
        self.location_x = location_x
        self.location_y = location_y

    def draw(self):
        display.blit(self.image, (self.location_x, self.location_y))
