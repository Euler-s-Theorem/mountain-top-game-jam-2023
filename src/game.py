import pygame


class Game:
    def __init__(self):
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.game_loop()
        pygame.quit()

    def update(self):
        pass

    def draw(self):
        pass

    def game_loop(self):
        # Update.
        self.update()
        # Draw.
        self.draw()
