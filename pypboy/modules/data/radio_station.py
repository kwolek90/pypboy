import os
from random import choice

import pygame

import config
import game


class RadioStation(game.Entity):

	STATES = {
		'stopped': 0,
		'playing': 1,
		'paused': 2
	}

	def __init__(self, directory, *args, **kwargs):
		self.directory = directory
		super(RadioStation, self).__init__((10, 10), *args, **kwargs)
		self.state = self.STATES['stopped']
		self.files = self.load_files()
		pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])


	def play_random(self):
		f = choice(self.files)
		self.filename = f
		pygame.mixer.music.load(f)
		pygame.mixer.music.play()
		self.state = self.STATES['playing']

	def play(self):
		if self.state == self.STATES['paused']:
			pygame.mixer.music.unpause()
			self.state = self.STATES['playing']
		else:
			self.play_random()

	def pause(self):
		self.state = self.STATES['paused']
		pygame.mixer.music.pause()

	def stop(self):
		self.state = self.STATES['stopped']
		pygame.mixer.music.stop()

	def load_files(self):
		files = []
		for f in os.listdir(self.directory):
			if f.endswith(".mp3") or f.endswith(".ogg") or f.endswith(".wav"):
				files.append(self.directory + f)
		print(files)
		return files