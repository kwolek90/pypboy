import pygame
import config
import game
import pypboy.header
import time

from pypboy.modules import data

if config.GPIO_AVAILABLE:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)

CLICK_DELAY = 500000000

class Pypboy(game.core.Engine):
	def __init__(self, *args, **kwargs):
		if hasattr(config, 'OUTPUT_WIDTH') and hasattr(config, 'OUTPUT_HEIGHT'):
			self.rescale = True
		super(Pypboy, self).__init__(*args, **kwargs)
		self.init_children()
		self.init_modules()
		self.last_pin_click = {}
		self.last_pause_click = time.time_ns()
		pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

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

		GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		self.last_pin_click = {
			5: time.time_ns(),
			6: time.time_ns(),
			16: time.time_ns(),
			26: time.time_ns()
		}

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
		if time.time_ns() - self.last_pause_click > CLICK_DELAY and not GPIO.input(6) and not GPIO.input(5):
			self.toogle_music()
			self.last_pause_click = time.time_ns()
		elif time.time_ns() - self.last_pin_click[6] > CLICK_DELAY and not GPIO.input(6):
			self.move_up()
			self.last_pin_click[6] = time.time_ns()
		elif time.time_ns() - self.last_pin_click[5] > CLICK_DELAY and not GPIO.input(5):
			self.move_down()
			self.last_pin_click[5] = time.time_ns()
		elif time.time_ns() - self.last_pin_click[16] > CLICK_DELAY and not GPIO.input(16):
			self.move_left()
			self.last_pin_click[16] = time.time_ns()
		elif time.time_ns() - self.last_pin_click[26] > CLICK_DELAY and not GPIO.input(26):
			self.move_right()
			self.last_pin_click[26] = time.time_ns()

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
