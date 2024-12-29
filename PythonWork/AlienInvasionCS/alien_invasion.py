import sys
import pygame

from settings import Settings

class AlienInvasion:
    '''This is a line comment'''

    def __init__(self):
        '''Initialize the game, and create game resources.'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((1200,800)) # change this later
        pygame.display.set_caption("Alien Invasion")

        # Set the background colour.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        '''Start the main loop for the game.'''
        while True:
            # Watch for the keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)
            
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    # Make the game instance, run the game
    ai = AlienInvasion()
    ai.run_game()
