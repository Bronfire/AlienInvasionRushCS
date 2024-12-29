import pygame

class Ship:
    '''A class to manage the ship'''
    def __init__(self, ai_game):
        '''Initialize the ship'''
        self.screen = ai_game.screen


def blitme(self):
    '''Draw the ship'''
    self.screen.blit(self.image, self.rect)
