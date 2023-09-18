import pygame
import game
import config
import pypboy.footer

if config.GPIO_AVAILABLE:
	import RPi.GPIO as GPIO


class BaseModule(game.EntityGroup):

	submodules = []

	def __init__(self, boy, *args, **kwargs):
		super(BaseModule, self).__init__()

		# if config.GPIO_AVAILABLE:
		# 	GPIO.setup(self.GPIO_LED_ID, GPIO.OUT)
		# 	GPIO.output(self.GPIO_LED_ID, True)

		self.pypboy = boy
		self.position = (0, 40)

		self.footer = pypboy.footer.Footer()
		self.footer.menu = []
		for mod in self.submodules:
			self.footer.menu.append(mod.label)
		self.footer.selected = self.footer.menu[0]
		self.footer.position = (0, config.HEIGHT - 53) #80
		self.add(self.footer)

		self.active = None
		self.active_module_index = 0
		self.switch_submodule(0)

		self.paused = True
		self.radio_station = None

		self.action_handlers = {
			"pause": self.handle_pause
		}
		if config.SOUND_ENABLED:
			self.module_change_sfx = pygame.mixer.Sound('sounds/module_change.ogg')

	def move(self, x, y):
		super(BaseModule, self).move(x, y)
		if hasattr(self, 'active'):
			self.active.move(x, y)

	def switch_submodule(self, module):
		if hasattr(self, 'active') and self.active:
			self.active.handle_action("pause")
			self.remove(self.active)
		if len(self.submodules) > module:
			self.active = self.submodules[module]
			self.active_module_index = module
			self.active.parent = self
			self.active.handle_action("resume")
			self.footer.select(self.footer.menu[module])
			self.add(self.active)
		else:
			print("No submodule at %d" % module)

	def render(self, interval):
		self.active.render(interval)
		super(BaseModule, self).render(interval)

	def handle_action(self, action, value=0):
		if action == "dial_right":
			num = (self.active_module_index + 1) % len(self.submodules)
			self.switch_submodule(num)
		if action == "dial_left":
			num = (self.active_module_index - 1) % len(self.submodules)
			self.switch_submodule(num)
		elif action in self.action_handlers:
			self.action_handlers[action]()
		else:
			if hasattr(self, 'active') and self.active:
				self.active.handle_action(action, value)

	def handle_event(self, event):
		if hasattr(self, 'active') and self.active:
			self.active.handle_event(event)

	def handle_pause(self):
		if config.radio and config.radio.active_station:
			config.radio.active_station.toogle()


class SubModule(game.EntityGroup):

	def __init__(self, parent, *args, **kwargs):
		super(SubModule, self).__init__()
		self.parent = parent

		self.action_handlers = {
			"pause": self.handle_pause,
			"resume": self.handle_resume
		}

		if config.SOUND_ENABLED:
			self.submodule_change_sfx = pygame.mixer.Sound('sounds/submodule_change.ogg')

	def handle_action(self, action, value=0):
		if action.startswith("dial_"):
			if hasattr(self, "menu"):
				self.menu.handle_action(action)
		elif action in self.action_handlers:
			self.action_handlers[action]()

	def handle_event(self, event):
		pass

	def handle_pause(self):
		self.paused = True

	def handle_resume(self):
		self.paused = False
		if config.SOUND_ENABLED:
			self.submodule_change_sfx.play()
