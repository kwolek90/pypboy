import pypboy
import pygame
import game
import config
import pypboy.menu
import time
import os

from PIL import Image, ImageSequence

class Module(pypboy.SubModule):
	label = "Status"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		health = Health()
		health.rect[0] = 4
		health.rect[1] = 40
		self.add(health)

		self.statuses = []
		self.statuses.append(Status("Version: " + config.VERSION, "Version: " + config.VERSION))
		self.selected_status = None

		handlers = []
		for x in range(len(self.statuses)):
			handlers.append(lambda x=x: self.select_status(x))

		self.menu = pypboy.menu.Menu(250, [x.name for x in self.statuses], handlers, 0)
		self.menu.rect[0] = 4
		self.menu.rect[1] = 50

		self.add(self.menu)

	def select_status(self, status_idx):
		if self.selected_status:
			self.selected_status.clear()
		status = self.statuses[status_idx]
		self.selected_status = status

	def update(self, *args, **kwargs):
		super(Module, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		if os.name == 'nt':
			temp = "No temp sensor"
		else:
			temp = os.popen("vcgencmd measure_temp").readline().upper().replace("=", " ").replace("'C\n", "°C")
		self.parent.pypboy.header.headline = "STATUS"
		self.parent.pypboy.header.title = temp
		super(Module, self).update()


def pilImageToSurface(pilImage):
	mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
	return pygame.image.fromstring(data, size, mode).convert_alpha()


def loadGIF(filename):
	pilImage = Image.open(filename)
	frames = []
	if pilImage.format == 'GIF' and pilImage.is_animated:
		for frame in ImageSequence.Iterator(pilImage):
			pygameImage = pilImageToSurface(frame.convert('RGBA'))
			frames.append(pygameImage)
	else:
		frames.append(pilImageToSurface(pilImage))
	return frames


class Health(game.Entity):
	def __init__(self):
		super(Health, self).__init__()
		self.last_render_time = 0
		self.rect = self.image.get_rect()

		self.gifFrameList = loadGIF("images/vault_boy_walking.gif")
		self.currentFrame = 0

	def render(self, *args, **kwargs):
		if self.last_render_time == 0:
			self.last_render_time = time.time()
			return
		else:
			interval = time.time() - self.last_render_time
			if interval < 0.05:
				return
			self.last_render_time = time.time()
			self.currentFrame = (self.currentFrame + 1) % len(self.gifFrameList)
		self.image = self.gifFrameList[self.currentFrame]
		self.rect = self.image.get_rect()
		self.rect.center = config.WIDTH//2, config.HEIGHT//2
		self.image.convert()
		return interval

	def update(self, *args, **kwargs):
		pass


class Status(game.Entity):
	def __init__(self, name, description, *args, **kwargs):
		super(Status, self).__init__((config.WIDTH, config.HEIGHT), *args, **kwargs)
		self.name = name
		self.text = description

	def render(self, *args, **kwargs):
		pass

	def update(self, *args, **kwargs):
		pass

	def print(self, *args, **kwargs):
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