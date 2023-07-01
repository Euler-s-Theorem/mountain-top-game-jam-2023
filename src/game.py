import pygame


class Game:
    def __init__(self):
        self.running = False
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 1

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
        pass

    def game_loop(self):
        # Update.
        self.update()
        # Draw.
        self.draw()
