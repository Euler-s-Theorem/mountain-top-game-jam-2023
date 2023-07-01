import pygame
import os
import json
from location import Location
from map import Map
import numpy as np


class Game:
    def __init__(self):
        self.running = False
        self.width = 1100
        self.height = 620
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.game_folder = os.path.dirname(__file__)
        self.map = Map(os.path.join(
            self.game_folder, "img", "map.png"))
        self.colour_bar = pygame.Rect(
            0, self.height*0.9, self.width, self.height/10)

        self.location_data = json.load(open(os.path.join(
            self.game_folder, "locations.json")))
        self.locations = []
        self.load_locations()
        self.current_location=None
        self.guess_list=[]

    def load_locations(self):
        directory = os.path.join(self.game_folder, "img", "locations")
        for file in os.listdir(directory):
            filepath = os.path.join(directory, file)
            map_x_and_y = self.location_data[file]
            location = Location(pygame.image.load(filepath), map_x_and_y['x'],
                                map_x_and_y['y'])
            self.locations.append(location)

    def distance(self, point1, point2):
        return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    
    def distance_to_colour(self, dist):
        normalized_distance=dist/np.sqrt(2) #sqrt(2) is the max distance on a square of length 1
        return pygame.Color(255, 0, 0,255)

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
        self.map.draw(self.window)
        pygame.draw.rect(self.window, 'gray', self.colour_bar)
        for guess in self.guess_list:
             pygame.draw.circle(self.window, self.distance_to_colour(self.distance((0,0), guess)), guess, 4)
             
        pygame.display.update()

    def game_loop(self):
        # Update.
        self.update()
        # Draw.
        self.draw()
