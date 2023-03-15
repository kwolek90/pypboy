import pygame

import config
import game


class Overlay(game.Entity):
	def __init__(self):
		self.image = pygame.image.load('images/overlay.png')
		super(Overlay, self).__init__((config.WIDTH, config.HEIGHT))
		self.blit_alpha(self, self.image, (0, 0), 128)

	def blit_alpha(self, target, source, location, opacity):
		x = location[0]
		y = location[1]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(target, (-x, -y))
		temp.blit(source, (0, 0))
		temp.set_alpha(opacity)
		target.blit(temp, location)