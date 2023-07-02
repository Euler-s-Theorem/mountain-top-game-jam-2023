import pygame
import os
import json
from location import Location
from map import Map
import numpy as np
import random


class Game:
    def __init__(self):
        self.running = False
        self.width = 1100
        self.height = 620
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 20
        self.game_folder = os.path.dirname(__file__)
        self.map = Map(os.path.join(
            self.game_folder, "img", "map.png"))
        self.colour_bar = pygame.Rect(
            0, self.height*0.9, self.width, self.height/10)
        self.game_bar = pygame.Rect(
            0, 0, self.width, self.height/10)
        self.location_data = json.load(open(os.path.join(
            self.game_folder, "locations.json")))
        self.locations = []
        self.current_location = None
        self.change_current_location_bool = False
        self.load_locations()
        self.guess_list = []
        # gameScreen = 0 is start screen mode, =1 is normal mode, 2 is endscreen mode
        self.gameScreen = 0
        self.score = 0

        self.buttons = {"startButton": (), "endButton": ()}

    def load_locations(self):
        directory = os.path.join(self.game_folder, "img", "locations")
        for file in os.listdir(directory):
            filepath = os.path.join(self.game_folder, "img", "locations", file)
            map_x_and_y = self.location_data[file]
            location = Location(filepath, map_x_and_y['x'],
                                map_x_and_y['y'])
            self.locations.append(location)

        random.shuffle(self.locations)

        if self.locations:
            self.current_location = self.locations[0]

    def distance(self, point1, point2):
        return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

    def distance_to_colour(self, dist):
        # distance should be between normalized points
        # sqrt(2) is the max distance on a square of length 1
        normalized_distance = dist/np.sqrt(2)
        return pygame.Color(int(255*(1-normalized_distance)), 0, int(255*normalized_distance), 255)

    def pixel_to_map_position(self, point):
        # converts a point represented by its pixel to normalized map coordinates
        # if the pixel is not on the map, returns (-1,-1)
        dimensions = self.map.getMapDimensions(self.window)
        map_x, map_y, map_width, map_height = dimensions[0], dimensions[1], dimensions[2], dimensions[3]
        if point[0] < map_x or point[0] > map_x+map_width or point[1] < map_y or point[1] > map_y+map_height:
            return (-1, -1)
        return ((point[0]-map_x)/map_width, (point[1]-map_y)/map_height)

    def map_position_to_pixel(self, point):
        # converts a point in normalized map coordinates to a pixel
        dimensions = self.map.getMapDimensions(self.window)
        map_x, map_y, map_width, map_height = dimensions[0], dimensions[1], dimensions[2], dimensions[3]
        return (int(point[0]*map_width+map_x), int(point[1]*map_height+map_y))

    def distance_to_message(self, dist):
        normalized_distance = dist/np.sqrt(2)
        real_map_width = self.map.get_real_map_width()
        # The average speed is 1.35 m/s
        time_away = int(normalized_distance*real_map_width/(1.35*60))
        message = ""
        if time_away == 0:
            message = "You got it!"
            self.change_current_location_bool = True
        elif time_away <= 5:
            message = "You're so close! You're " + \
                str(time_away)+" minutes away."
        elif time_away <= 10:
            message = "Getting warmer. You're "+str(time_away)+" minutes away."
        elif time_away <= 20:
            message = "Not quite. You're " + str(time_away)+" minutes away."
        else:
            message = "You're way off. You're " + \
                str(time_away)+" minutes away."
        if self.guess_list:
            message += str(np.round(self.guess_list[-1], 3))
        return message

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
                position = self.pixel_to_map_position(pygame.mouse.get_pos())
                if self.gameScreen == 1:
                    if position != (-1, -1):
                        self.guess_list.append(position)
                elif self.gameScreen == 0:
                    pass

    def current_location_changer(self):
        if self.change_current_location_bool:
            # get current index of current image being displayed
            current_location_index = self.locations.index(
                self.current_location)
            if current_location_index < len(self.locations):
                current_location_index += 1
                self.current_location = self.locations[current_location_index]
                # increase score
                points = 100 - np.exp(1) ** (len(self.guess_list) - 1)
                if points < 5:
                    points = 5
                self.score += int(points)
                # empty guess list
                self.guess_list = []
            else:
                pass  # should be game over msg since no more pics
            self.change_current_location_bool = False

    def draw(self):
        pygame.font.init()  # initilize font
        print(self.buttons)
        if (self.gameScreen == 0):
            # the start screen
            self.window.fill("white")

            # the title text part
            topBanner = pygame.Rect(0, 0, self.width, self.height*.2)
            pygame.draw.rect(self.window, 'skyblue', topBanner)
            title_text = pygame.font.SysFont('Arial', 45).render(
                "How well do you know the tallest Peak in Burnaby?", True, "black")
            title_text_rext = title_text.get_rect()
            title_text_rext.center = (self.width/2, self.height/2-250)
            pygame.draw.rect(self.window, "skyblue", title_text_rext)
            self.window.blit(title_text, title_text_rext)

            # get img in middle
            burnaby_mountain_image = pygame.image.load(
                os.path.join(self.game_folder, "img", "Burnaby_Mountain.jpg"))
            burnaby_mountain_image = pygame.transform.smoothscale_by(
                burnaby_mountain_image, .15)
            self.window.blit(burnaby_mountain_image, (0, self.height*.2))

            bottomBanner = pygame.Rect(
                0, self.height*.8, self.width, self.height*.3)
            pygame.draw.rect(self.window, 'skyblue', bottomBanner)

            # start button
            startButtonText = pygame.font.SysFont(
                'Arial', 75).render(" Start ", True, "black")
            startButton = startButtonText.get_rect()
            startButton.center = (self.width*.3, self.height/2+250)
            pygame.draw.rect(self.window, "blue", startButton)
            self.window.blit(startButtonText, startButton)
            self.buttons["startButton"] = (
                startButton.top, startButton.left, startButton.bottom, startButton.right)
            # help button
            helpButtonText = pygame.font.SysFont(
                'Arial', 75).render(" Help ", True, "black")
            helpButton = helpButtonText.get_rect()
            helpButton.center = (self.width*.7, self.height/2+250)
            pygame.draw.rect(self.window, "lightgreen", helpButton)
            self.window.blit(helpButtonText, helpButton)
            self.buttons["helpButton"] = (
                helpButton.top, helpButton.left, helpButton.bottom, helpButton.right)
        else:
            # gamebar
            pygame.draw.rect(self.window, 'skyblue', self.game_bar)

            font = pygame.font.SysFont('Arial', 30)
            guess_text = font.render(
                "Guesses Used: " + str(len(self.guess_list)), True, "black")
            self.window.blit(guess_text, (5, 10))

            points_text = font.render(
                "Score:  " + str(self.score), True, "black")
            self.window.blit(points_text, (self.width*.85, 10))
            # add map to game
            self.map.draw(self.window)

            # draw image of location
            self.current_location.draw(self.window)

            # color bar
            # draw guesss
            for guess in self.guess_list:
                pygame.draw.circle(self.window, self.distance_to_colour(self.distance(self.current_location.get_position(), guess)),
                                   self.map_position_to_pixel(guess), 4)
            self.draw_colorbar_message()

            # check if user found right answer
            self.current_location_changer()

        pygame.display.update()

    def draw_colorbar_message(self):
        pygame.font.init()  # initilize font
        font = pygame.font.SysFont('Arial', 30)
        if len(self.guess_list) > 0:
            pygame.draw.rect(self.window, self.distance_to_colour(
                self.distance(self.current_location.get_position(), self.guess_list[-1])), self.colour_bar)
            message = self.distance_to_message(
                self.distance(self.current_location.get_position(), self.guess_list[-1]))

            message_text = font.render(message, True, "black")
            self.window.blit(message_text, (5, self.height*0.92))
        else:
            pygame.draw.rect(self.window, "gray", self.colour_bar)
            message_text = font.render(
                "Guess where the picture was taken from by clicking on the map.", True, "black")
            self.window.blit(message_text, (5, self.height*0.92))

    def game_loop(self):
        # Update.
        self.update()
        # Draw.
        self.draw()

# bottom isnt done yet
    def check_if_position_in_domain(mousePostion, domain):
        if mousePostion[1] <= domain[3] and mousePostion[1] >= domain[1] and mousePostion[2] >= domain[1] and mousePostion[2] >= domain[4]:
            return True
        return False
