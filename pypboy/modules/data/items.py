import pypboy
import pygame
import game
import config
import os


class Module(pypboy.SubModule):

	label = "Items"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)

		self.items = []
		self.items.append(Item("Żółty proszek", "Robiony z elektroniki", 5))
		self.items.append(Item("Stimpack", "Do leczenia ran", 1, "stimpak.png"))
		self.items.append(Item("Złom", "Podstawowy materiał budulcowy rzeczy", 2))
		self.items.append(Item("Kapsle", "Waluta", 36))
		self.selected_item = None

		for item in self.items:
			self.add(item)

		handlers = []
		for x in range(len(self.items)):
			handlers.append(lambda x=x: self.select_item(x))

		self.menu = pypboy.menu.Menu(250, [x.name for x in self.items], handlers, 0)
		self.menu.rect[0] = 4
		self.menu.rect[1] = 50

		self.add(self.menu)

	def select_item(self, item_idx):
		if self.selected_item:
			self.selected_item.clear()
		item = self.items[item_idx]

		item.print()
		self.selected_item = item


class Item(game.Entity):
	def __init__(self, name, description, amount, icon=None, *args, **kwargs):
		super(Item, self).__init__((config.WIDTH, config.HEIGHT), *args, **kwargs)
		self.name = name
		self.text = description
		self.amount = amount
		self.icon = icon

	def render(self, *args, **kwargs):
		pass

	def update(self, *args, **kwargs):
		pass

	def print(self, *args, **kwargs):
		if self.icon is not None:
			icon = pygame.image.load(os.path.join(config.ICONS_DIRECTORY, self.icon))
			self.image.blit(icon, (150, 50))

		font_size = 8
		line_length = int((config.WIDTH - 150) / (font_size / 2))


		text = ""
		line_idx = 0
		for line in self.text.splitlines():
			for word in line.split():
				if len(word) + len(text) > line_length:
					self.image.blit(config.FONTS[font_size].render(text, True, (105, 255, 187), (0, 0, 0)),
									(140, 50 + line_idx * font_size))
					text = ""
					line_idx += 1
				text += word + " "
			self.image.blit(config.FONTS[font_size].render(text, True, (105, 255, 187), (0, 0, 0)),
							(140, 50 + line_idx * font_size))
			text = ""
			line_idx += 1

	def clear(self):
		self.image.fill((0, 0, 0))