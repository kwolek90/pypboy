import pygame

import config
import game


class Footer(game.Entity):

	def __init__(self):
		self.menu = []
		super(Footer, self).__init__((config.WIDTH, config.HEIGHT))
		self.rect[0] = 4
		self.rect[1] = config.HEIGHT - 40

	def update(self, *args, **kwargs):
		super(Footer, self).update(*args, **kwargs)

	def select(self, module):
		#self.dirty = 1
		self.selected = module
		self.image.fill((0, 0, 0))
		pygame.draw.line(self.image, (95, 255, 177), (5, 2), (5, 20), 2)
		pygame.draw.line(self.image, (95, 255, 177), (5, 20), (config.WIDTH - 13, 20), 2)
		pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 13, 2), (config.WIDTH - 13, 20), 2)

		offset = 10
		for m in self.menu:
			padding = 1
			text_width = 0
			while text_width < 50:
				spaces = " ".join([" " for x in range(padding)])
				text = config.FONTS[12].render("%s%s%s" % (spaces, m, spaces), True, (105, 255, 187), (0, 0, 0))
				text_width = text.get_size()[0]
				padding += 1

			if m == self.selected:
				pygame.draw.rect(self.image, (95, 255, 177), (offset - 2, 6, (text_width + 3), 26), 2)
			self.image.blit(text, (offset, 12))

			offset = offset + 110 + (text_width - 100)
