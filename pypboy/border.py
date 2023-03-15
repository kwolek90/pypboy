import pygame

import game


class Border(game.Entity):
	def __init__(self):
		super(Border, self).__init__()
		self.image = pygame.image.load('images/border.png')
		self.rect = self.image.get_rect()