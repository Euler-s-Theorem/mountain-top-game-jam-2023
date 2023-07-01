import pygame


class Map:
    def __init__(self, imagePath):
        # grab the images and scales it before storing into self.image
        self.image = pygame.transform.scale_by(
            pygame.image.load(imagePath), .3)

    def draw(self, window):
        main_width = window.get_width()
        main_height = window.get_height()

        # draw mapground for map
        pygame.draw.rect(window, "white", pygame.Rect(
            main_width*.35, main_height*.1, main_width*.65, main_height*.8))
        # draw map
        window.blit(self.image, (main_width*.35, main_height*.1))
