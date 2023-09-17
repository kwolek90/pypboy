import pygame
import config
import game
import pypboy.header
import time

from pypboy.modules import data

if config.GPIO_AVAILABLE:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)

PAUSE_PIN = 19


class Dial:
	def __init__(self, clk, dt, left_action, right_action, pipboy):
		self.Enc_A = clk
		self.Enc_B = dt
		self.left_action = left_action
		self.right_action = right_action
		self.pipboy = pipboy

		GPIO.setmode(GPIO.BCM)

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.Enc_A, GPIO.IN)
		GPIO.setup(self.Enc_B, GPIO.IN)
		GPIO.add_event_detect(self.Enc_A, GPIO.RISING, callback=self.rotation_decode, bouncetime=100)

	def rotation_decode(self, Enc_A):
		time.sleep(0.002)
		Switch_A = GPIO.input(self.Enc_A)
		Switch_B = GPIO.input(self.Enc_B)

		if (Switch_A == 1) and (Switch_B == 0):
			self.pipboy.handle_action(self.left_action)
			# while Switch_B == 0:
			# 	Switch_B = GPIO.input(self.Enc_B)
			# while Switch_B == 1:
			# 	Switch_B = GPIO.input(self.Enc_B)
			time.sleep(0.5)
			return

		elif (Switch_A == 1) and (Switch_B == 1):
			self.pipboy.handle_action(self.right_action)
			# while Switch_A == 1:
			# 	Switch_A = GPIO.input(self.Enc_A)
			time.sleep(0.5)
			return
		else:
			time.sleep(0.1)
			return


class Pypboy(game.core.Engine):
	def __init__(self, *args, **kwargs):
		if hasattr(config, 'OUTPUT_WIDTH') and hasattr(config, 'OUTPUT_HEIGHT'):
			self.rescale = True
		super(Pypboy, self).__init__(*args, **kwargs)
		self.init_children()
		self.init_modules()
		self.last_pause_click = time.time_ns()

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
		self.dial_hor = Dial(5, 6, "dial_left", "dial_right", self)
		self.dial_vert = Dial(20, 21, "dial_down", "dial_up", self)
		GPIO.setup(PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.gpio_actions[PAUSE_PIN] = "pause"

	def check_gpio_input(self):
		if time.time_ns() - self.last_pause_click > 500000000 and not GPIO.input(PAUSE_PIN):
			self.handle_action("pause")
			self.last_pause_click = time.time_ns()
			print("pause")

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
