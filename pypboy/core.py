import pygame
import config
import game
import pypboy.header
import time

from pypboy.modules import data

if config.GPIO_AVAILABLE:
	from pyky040 import pyky040
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)


class Pypboy(game.core.Engine):
	def __init__(self, *args, **kwargs):
		if hasattr(config, 'OUTPUT_WIDTH') and hasattr(config, 'OUTPUT_HEIGHT'):
			self.rescale = True
		super(Pypboy, self).__init__(*args, **kwargs)
		self.init_children()
		self.init_modules()
		self.last_pause_click = time.time_ns()
		#pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

		self.gpio_actions = {}
		if config.GPIO_AVAILABLE:
			self.init_gpio_controls()

	def init_children(self):
		self.background = pygame.image.load('images/overlay.png')
		self.header = pypboy.header.Header()
		self.root_children.add(self.header)

	def init_modules(self):
		self.modules = {
			"data": data.Module(self),
		}
		for module in self.modules.values():
			module.move(4, 40)
		self.switch_module("data")

	def init_gpio_controls(self):
		GPIO.setmode(GPIO.BCM)

		encoder = pyky040.Encoder(CLK=5, DT=6, SW=21)
		encoder.setup(scale_min=0, scale_max=100, step=1, inc_callback=self.move_right, dec_callback=self.move_left, sw_callback=self.toogle_music, sw_debounce_time=500)
		encoder.watch()
		my_encoder = pyky040.Encoder(CLK=26, DT=19, SW=20)
		my_encoder.setup(scale_min=0, scale_max=100, step=1, inc_callback=self.move_up, dec_callback=self.move_down, sw_callback=self.toogle_music, sw_debounce_time=250)
		my_encoder.watch()

	def move_left(self):
		self.handle_action("dial_left")

	def move_right(self):
		self.handle_action("dial_right")

	def move_up(self):
		self.handle_action("dial_up")

	def move_down(self):
		self.handle_action("dial_down")

	def toogle_music(self):
		self.handle_action("pause")

	def check_gpio_input(self):
		pass
		# if time.time_ns() - self.last_pause_click > 500000000 and not GPIO.input(PAUSE_PIN):
		# 	self.handle_action("pause")
		# 	self.last_pause_click = time.time_ns()
		# 	print("pause")

	def update(self):
		if hasattr(self, 'active'):
			self.active.update()
		super(Pypboy, self).update()

	def render(self):
		interval = super(Pypboy, self).render()
		if hasattr(self, 'active'):
			self.active.render(interval)

	def switch_module(self, module):
		if module in self.modules:
			if hasattr(self, 'active'):
				self.active.handle_action("pause")
				self.remove(self.active)
			self.active = self.modules[module]
			self.active.parent = self
			self.active.handle_action("resume")
			self.add(self.active)
			print("Active module %s", module)
		else:
			print("Module '%s' not implemented." % module)

	def handle_action(self, action):
		if action.startswith('module_'):
			self.switch_module(action[7:])
		else:
			if hasattr(self, 'active'):
				self.active.handle_action(action)

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_ESCAPE):
				self.running = False
			else:
				if event.key in config.ACTIONS:
					self.handle_action(config.ACTIONS[event.key])
		elif event.type == pygame.QUIT:
			self.running = False
		elif event.type == config.EVENTS['SONG_END']:
			if hasattr(config, 'radio'):
				config.radio.handle_event(event)
		else:
			if hasattr(self, 'active'):
				self.active.handle_event(event)

	def run(self):
		self.running = True
		while self.running:
			for event in pygame.event.get():
				self.handle_event(event)
			self.update()
			self.render()
			if config.GPIO_AVAILABLE:
				self.check_gpio_input()
			pygame.time.wait(10)

		try:
			pygame.mixer.quit()
		except:
			pass
