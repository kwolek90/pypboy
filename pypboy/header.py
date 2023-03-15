import datetime

import pygame

import config
import game


class Header(game.Entity):

	def __init__(self, headline="", title=""):
		self.headline = headline
		self.title = title
		super(Header, self).__init__((config.WIDTH, config.HEIGHT))
		self.rect[0] = 4
		self._date = None

	def update(self, *args, **kwargs):
		super(Header, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		new_date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
		if new_date != self._date:
			self.image.fill((0, 0, 0))
			pygame.draw.line(self.image, (95, 255, 177), (5, 15), (5, 35), 2)
			pygame.draw.line(self.image, (95, 255, 177), (5, 15), (config.WIDTH - 154, 15), 2)
			pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 154, 15), (config.WIDTH - 154, 35), 2)
			pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 148, 15), (config.WIDTH - 13, 15), 2)
			pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 13, 15), (config.WIDTH - 13, 35), 2)

			text = config.FONTS[14].render("  %s  " % self.headline, True, (105, 251, 187), (0, 0, 0))
			self.image.blit(text, (26, 8))
			text = config.FONTS[14].render(self.title, True, (95, 255, 177), (0, 0, 0))
			self.image.blit(text, ((config.WIDTH - 154) - text.get_width() - 10, 19))
			text = config.FONTS[14].render(self._date, True, (95, 255, 177), (0, 0, 0))
			self.image.blit(text, ((config.WIDTH - 141), 19))
			self._date = new_date

		super(Header, self).update(*args, **kwargs)