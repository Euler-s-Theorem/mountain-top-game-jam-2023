import pygame
import os


class Game:
    def __init__(self):
        self.running = False
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.game_folder = os.path.dirname(__file__)
        self.guess_image = pygame.image.load(os.path.join(
            self.game_folder, "img", "testImg.png"))
        self.map = pygame.image.load(os.path.join(
            self.game_folder, "img", "map.png"))

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
                pos = pygame.mouse.get_pos()
                print(pos)

    def draw(self):
        # add map to game
        self.window.blit(self.map, (0, 0))
        #

        pygame.display.update()

    def game_loop(self):
        # Update.
        self.update()
        # Draw.
        self.draw()
