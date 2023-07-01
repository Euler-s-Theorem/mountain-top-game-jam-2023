import pygame


class Map:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)

    def draw(self, window):
        # add map to game
        window.blit(self.image, (0, 0))
