import pygame
import os
from location import Location
from map import Map


class Game:
    def __init__(self):
        self.running = False
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.game_folder = os.path.dirname(__file__)
        self.map = Map(os.path.join(
            self.game_folder, "img", "map.png"))
        self.colour_bar = pygame.Rect(
            0, self.height*0.9, self.width, self.height/10)

        self.locations = []
        self.load_locations()

        self.guess_list = []

    def load_locations(self):
        for file in os.listdir(os.path.join(
                self.game_folder, "img", "locations")):
            self.locations.append(Location.from_filename(file))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(self.fps)
            self.game_loop()
        pygame.quit()

    def update(self):
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.guess_list.append(pygame.mouse.get_pos())

    def draw(self):
        # add map to game
        self.window.blit(self.map, (0, 0))
        pygame.draw.rect(self.window, 'gray', self.colour_bar)
        for guess in self.guess_list:
            pygame.draw.rect(self.window, 'blue', pygame.Rect(
                guess[0], guess[1], 10, 10))
        self.map.draw(self.window)

        pygame.display.update()

    def game_loop(self):
        # Update.
        self.update()
        # Draw.
        self.draw()
