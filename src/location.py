import pygame


class Location:
    def __init__(self, imagePath, map_x=0, map_y=0):

        self.image = pygame.transform.smoothscale_by(
            pygame.image.load(imagePath), .08)
        self.image = pygame.transform.rotate(self.image, 270)

        # cordinates of location in the map
        self.map_x = map_x
        self.map_y = map_y

    def get_position(self):
        return self.map_x, self.map_y

    def draw(self, window):
        main_width = window.get_width()
        main_height = window.get_height()

        # draw background for image
        pygame.draw.rect(window, "skyblue", pygame.Rect(
            0, main_height*.1, main_width*.35, main_height*.8))

        # center image to center of left side
        image_rect = self.image.get_rect()
        left_side_center_x = (main_width*.35)/2
        left_side_center_y = (main_height*.9 - main_height*0)/2
        image_rect.center = (left_side_center_x, left_side_center_y)
        window.blit(self.image, image_rect)

    def __str__(self):
        return f"Location with image {self.image} at ({self.map_x}, {self.map_y})"
