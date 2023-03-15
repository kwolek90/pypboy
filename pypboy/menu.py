import pygame

import config
import game


class Menu(game.Entity):

	def __init__(self, width, items=[], callbacks=[], selected=0):
		super(Menu, self).__init__((width, config.HEIGHT - 80))
		self.items = items
		self.callbacks = callbacks
		self.selected = 0
		self.select(selected)

		if config.SOUND_ENABLED:
			self.dial_move_sfx = pygame.mixer.Sound('sounds/dial_move.ogg')

	def select(self, item):
		self.selected = item
		self.redraw()
		if len(self.callbacks) > item and self.callbacks[item]:
			self.callbacks[item]()

	def handle_action(self, action):
		if action == "dial_up":
			if self.selected > 0:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.select(self.selected - 1)
		if action == "dial_down":
			if self.selected < len(self.items) - 1:
				if config.SOUND_ENABLED:
					self.dial_move_sfx.play()
				self.select(self.selected + 1)

	def redraw(self):
		self.image.fill((0, 0, 0))
		offset = 5
		for i in range(len(self.items)):
			text = config.FONTS[14].render(" %s " % self.items[i], True, (105, 255, 187), (0, 0, 0))
			if i == self.selected:
				selected_rect = (5, offset - 2, text.get_size()[0] + 6, text.get_size()[1] + 3)
				pygame.draw.rect(self.image, (95, 255, 177), selected_rect, 2)
			self.image.blit(text, (10, offset))
			offset += text.get_size()[1] + 6