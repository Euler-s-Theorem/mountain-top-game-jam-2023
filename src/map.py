import pygame


class Map:
    def __init__(self, imagePath):
        self.image = pygame.image.load(imagePath)

    def draw(self, window):
        # add map to game
        window.blit(self.image, (0, 0))
