import pygame
import config
import game
import pypboy.header

from pypboy.modules import data

if config.GPIO_AVAILABLE:
	import RPi.GPIO as GPIO


class Dial:
	def __init__(self, clk, dt, left_action, right_action):
		self.clk = clk
		self.dt = dt
		self.left_action = left_action
		self.right_action = right_action
		self.clkLastState = GPIO.input(self.clk)
		GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def handle(self, pipboy):
		clkState = GPIO.input(self.clk)
		dtState = GPIO.input(self.dt)
		if clkState != self.clkLastState:
			if dtState != clkState:
				self.pipboy.handle_action(self.left_action)
			else:
				self.pipboy.handle_action(self.right_action)
		self.clkLastState = clkState


class Pypboy(game.core.Engine):

	def __init__(self, *args, **kwargs):
		if hasattr(config, 'OUTPUT_WIDTH') and hasattr(config, 'OUTPUT_HEIGHT'):
			self.rescale = True
		super(Pypboy, self).__init__(*args, **kwargs)
		self.init_children()
		self.init_modules()
		
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
		self.dial_hor = Dial(5, 6, "dial_left", "dial_right")
		self.dial_vert = Dial(31, 27, "dial_down", "dial_up")
		GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.gpio_actions[26] = "pause"

	def check_gpio_input(self):
		if not GPIO.input(26):
			self.handle_action("pause")
		self.dial_vert.handle(self)
		self.dial_hor.handle(self)

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
			self.check_gpio_input()
			pygame.time.wait(10)

		try:
			pygame.mixer.quit()
		except:
			pass
