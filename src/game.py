import pygame
import os
import json
from location import Location
from map import Map
import numpy as np
import random
import time
import threading


class Game:
    def __init__(self):
        self.running = False
        self.width = 1100
        self.height = 600
        self.min_width = 1000
        self.min_height = 550
        self.window = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Peak Guesser")
        self.fps = 30
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
        self.number_of_locations = 8
        self.load_locations()
        self.guess_list = []
        # gameScreen = 0 is start screen mode, =1 is normal mode, 2 is endscreen mode
        self.gameScreen = 0
        self.score = 0

        self.buttons = {
            "startButton": (-1, -1, -1, -1), "playAgainButton": {-1, -1, -1, -1}}
        self.booleans = {"Change_current_location": False}

    def load_locations(self):
        # draw loading screen first
        self.window.fill("white")
        pygame.font.init()  # initilize font
        # topBanner = pygame.Rect(0, 0, self.width, self.height*.2)
        # pygame.draw.rect(self.window, 'skyblue', topBanner)
        title_text = pygame.font.SysFont('Arial', 65).render(
            "Loading....", True, "black")
        title_text_rext = title_text.get_rect()
        title_text_rext.center = (self.width/2, self.height/2)
        pygame.draw.rect(self.window, "white", title_text_rext)
        self.window.blit(title_text, title_text_rext)
        pygame.display.update()

        directory = os.path.join(self.game_folder, "img", "locations")
        image_names = os.listdir(directory)
        random_location_indices = random.sample(
            range(len(image_names)), self.number_of_locations)
        for i in range(self.number_of_locations):
            file = image_names[random_location_indices[i]]
            filepath = os.path.join(self.game_folder, "img", "locations", file)
            map_x_and_y = self.location_data[file]
            location = Location(filepath, map_x_and_y['x'],
                                map_x_and_y['y'])
            self.locations.append(location)

        if self.locations:
            self.current_location = self.locations[0]

    def distance(self, point1, point2):
        return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

    def distance_to_colour(self, dist):
        # distance should be between normalized points
        # sqrt(2) is the max distance on a square of length 1
        normalized_distance = dist
        if dist > 1:
            normalized_distance = 1
        if normalized_distance < 0.5:
            return pygame.Color(int(255*normalized_distance*2), 255, 0)
        else:
            return pygame.Color(255, int(2*255*(1-normalized_distance)), 0)

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
        if time_away <= 1:
            message = "You got it!"
            self.booleans["Change_current_location"] = True
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if self.gameScreen == 1:
                    position = self.pixel_to_map_position(
                        pygame.mouse.get_pos())
                    if position != (-1, -1):
                        self.guess_list.append(position)
                if self.gameScreen == 0:
                    if self.check_if_position_in_domain(position, self.buttons["startButton"]):
                        self.gameScreen = 1
                if self.gameScreen == 2:
                    if self.check_if_position_in_domain(position, self.buttons["playAgainButton"]):
                        self.score = 0
                        self.gameScreen = 0
                        self.score = 0
                        self.load_locations()
                        """elif self.check_if_position_in_domain(pygame.mouse.get_pos(), self.buttons["helpButton"]):
                            self.gameScreen = 1"""

            elif event.type == pygame.VIDEORESIZE:
                self.width = event.size[0]
                self.height = event.size[1]
                if self.width < self.min_width or self.height < self.min_height:
                    self.width = max(self.width, self.min_width)
                    self.height = max(self.height, self.min_height)
                    pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE)

    def current_location_changer(self):
        if self.booleans["Change_current_location"]:
            # get current index of current image being displayed
            current_location_index = self.locations.index(
                self.current_location)
            if current_location_index < len(self.locations) - 1:
                current_location_index += 1
                self.current_location = self.locations[current_location_index]
            else:
                self.gameScreen = 2
            # increase score
            points = 100 - np.exp((len(self.guess_list) - 1)) + 1
            points += np.sqrt(np.pi * points ** 2 + 1)
            points = int(points)
            if points < 5:
                points = 5
            self.score += int(points)
            # empty guess list
            self.guess_list = []

            self.booleans["Change_current_location"] = False

    def draw(self):
        pygame.font.init()  # initilize font
        self.width, self.height = self.window.get_size()

        self.window.fill("white")
        if (self.gameScreen == 0):
            self.drawHomeScreen()
        elif self.gameScreen == 1:
            # gamebar
            self.game_bar = pygame.Rect(0, 0, self.width, self.height/10)
            pygame.draw.rect(self.window, 'skyblue', self.game_bar)

            font = pygame.font.SysFont('Arial', 30)
            guess_text = font.render(
                "Guesses Used: " + str(len(self.guess_list)), True, "black")
            self.window.blit(guess_text, (5, 10))

            points_text = font.render(
                "Score:  " + str(self.score), True, "black")
            self.window.blit(points_text, (self.width*.7, 10))
            # add map to game
            self.map.draw(self.window)

            # draw image of location
            self.current_location.draw(self.window)

            # color bar
            # draw guesss
            for guess in self.guess_list:
                pygame.draw.circle(self.window, self.distance_to_colour(self.distance(self.current_location.get_position(), guess)),
                                   self.map_position_to_pixel(guess), 8)
            self.draw_colorbar_message()

            # check if user found right answer
            self.current_location_changer()
        elif self.gameScreen == 2:
            self.drawEndScreen()
        pygame.display.update()

    def draw_colorbar_message(self):
        pygame.font.init()  # initilize font

        font = pygame.font.SysFont('Arial', 30)
        if len(self.guess_list) > 0:
            self.colour_bar = pygame.Rect(
                0, self.height*0.9, self.width, self.height/10)
            pygame.draw.rect(self.window, self.distance_to_colour(
                self.distance(self.current_location.get_position(), self.guess_list[-1])), self.colour_bar)
            message = self.distance_to_message(
                self.distance(self.current_location.get_position(), self.guess_list[-1]))
            message_text = font.render(message, True, "black")
            self.window.blit(
                message_text, self.colour_bar)  # (5, self.height*0.92)

            # if "You got it!" in message:
            #    time.sleep(1.5)
        else:
            self.colour_bar = pygame.Rect(
                0, self.height*0.9, self.width, self.height/10)
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
    def check_if_position_in_domain(self, mousePostion, domain):

        if mousePostion[0] <= domain[3] and mousePostion[0] >= domain[1] and mousePostion[1] >= domain[1] and mousePostion[1] <= domain[2]:
            return True
        return False

    def drawHomeScreen(self):
        # the start screen
        self.window.fill("white")

        # the title text part
        topBanner = pygame.Rect(0, 0, self.width, self.height*.2)
        pygame.draw.rect(self.window, 'skyblue', topBanner)
        title_text = pygame.font.SysFont('Arial', 45).render(
            "How well do you know the tallest Peak in Burnaby?", True, "black")
        title_text_rext = title_text.get_rect()
        title_text_rext.center = (self.width/2, 75)
        pygame.draw.rect(self.window, "skyblue", title_text_rext)
        self.window.blit(title_text, title_text_rext)

        # get img in middle
        burnaby_mountain_image = pygame.image.load(
            os.path.join(self.game_folder, "img", "Burnaby_Mountain.jpg"))
        burnaby_mountain_image = pygame.transform.smoothscale_by(
            burnaby_mountain_image, .25)
        self.window.blit(burnaby_mountain_image, (0, self.height*.2))

        bottomBanner = pygame.Rect(
            0, self.height*.8, self.width, self.height*.3)
        pygame.draw.rect(self.window, 'skyblue', bottomBanner)

        # start button
        startButtonText = pygame.font.SysFont(
            'Arial', 75).render(" Start ", True, "black")
        startButton = startButtonText.get_rect()
        startButton.center = (self.width*.5, self.height*.91)
        pygame.draw.rect(self.window, "blue", startButton)
        self.window.blit(startButtonText, startButton)
        self.buttons["startButton"] = (
            startButton.top, startButton.left, startButton.bottom, startButton.right)
        # help button
        """
        helpButtonText = pygame.font.SysFont(
            'Arial', 75).render(" Help ", True, "black")
        helpButton = helpButtonText.get_rect()
        helpButton.center = (self.width*.7, self.height/2+250)
        pygame.draw.rect(self.window, "lightgreen", helpButton)
        self.window.blit(helpButtonText, helpButton)
        self.buttons["helpButton"] = (
            helpButton.top, helpButton.left, helpButton.bottom, helpButton.right)"""

    def drawEndScreen(self):
        self.window.fill("skyblue")
        # the title text part
        topBanner = pygame.Rect(0, 0, self.width, self.height*.2)
        pygame.draw.rect(self.window, 'skyblue', topBanner)
        title_text = pygame.font.SysFont('Arial', 45).render(
            "Game over, You have scored " + str(self.score) + " points!", True, "black")
        title_text_rext = title_text.get_rect()
        title_text_rext.center = (self.width/2, self.height/2-250)
        pygame.draw.rect(self.window, "skyblue", title_text_rext)
        self.window.blit(title_text, title_text_rext)

        # restart button
        playAgainButtonText = pygame.font.SysFont(
            'Arial', 75).render(" Play Again ", True, "black")
        playAgainButton = playAgainButtonText.get_rect()
        playAgainButton.center = (self.width*.5, self.height*.6)
        pygame.draw.rect(self.window, "red", playAgainButton)
        self.window.blit(playAgainButtonText, playAgainButton)
        self.buttons["playAgainButton"] = (
            playAgainButton.top, playAgainButton.left, playAgainButton.bottom, playAgainButton.right)
