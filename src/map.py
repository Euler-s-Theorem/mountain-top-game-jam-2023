import pygame


class Map:
    def __init__(self, imagePath):
        # grab the images and scales it before storing into self.image
        self.image = pygame.transform.smoothscale_by(
            pygame.image.load(imagePath), .63)
        # width of the area on the map in real life, in meters
        self.real_map_width = 2650

    def draw(self, window):
        main_width = window.get_width()
        main_height = window.get_height()
        # draw mapground for map
        pygame.draw.rect(window, "skyblue", pygame.Rect(
            main_width*.35, main_height*.1, main_width*.65, main_height*.8))
        # draw map
        window.blit(self.image, (main_width*.35, main_height*.2))

    def getMapDimensions(self, window):
        main_width = window.get_width()
        main_height = window.get_height()
        return (main_width*.35, main_height*.2, self.image.get_width(), self.image.get_height())

    def get_real_map_width(self):
        return self.real_map_width
