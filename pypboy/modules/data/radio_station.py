import os
from random import choice

import pygame

import config
import game
import time
import pickle


class RadioStation(game.Entity):

	STATES = {
		'stopped': 0,
		'playing': 1,
		'paused': 2
	}

	def __init__(self, directory, *args, **kwargs):
		self.name = os.path.split(os.path.dirname(directory))[-1]
		self.directory = directory
		super(RadioStation, self).__init__((config.WIDTH, config.HEIGHT), *args, **kwargs)
		self.state = self.STATES['stopped']
		self.files = self.load_files()
		self.oscilloscope_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
		pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])
		self.stream = None
		self.filename = None
		self.getTicksLastFrame = 0
		self.bars = []
		self.spectrogram = None
		self.frequencies_index_ratio = None
		self.time_index_ratio = None
		self.last_render_time = 0
		self.spectrogram = None

	def play_random(self):
		self.filename = choice(self.files)
		pygame.mixer.music.load(self.filename)
		pygame.mixer.music.play()
		self.state = self.STATES['playing']
		print(self.filename)

		self.spectrogram = Spectrogram(self.filename)
		self.bars = self.spectrogram.bars

	def render(self, *args, **kwargs):
		if self.last_render_time == 0:
			self.last_render_time = time.time()
			return
		else:
			interval = time.time() - self.last_render_time
			if interval < 0.1:
				return

		for b in self.bars:
			b.update(self.spectrogram.get_decibel(pygame.mixer.music.get_pos() / 1000.0, b.freq))
			b.render(self.image)

		self.last_render_time = time.time()

	def toogle(self):
		if self.state == self.STATES['playing']:
			self.pause()
		else:
			self.play()

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
		if not config.GPIO_ACTIONS:
			for filename in files:
				if not os.path.isfile(os.path.splitext(filename)[0] + ".dump"):
					print(filename)
					Spectrogram(filename, True)
		return files


def clamp(min_value, max_value, value):
	if value < min_value:
		return min_value

	if value > max_value:
		return max_value

	return value


class Spectrogram:
	def __init__(self, filename, prepare=False):
		dump_file = os.path.splitext(filename)[0] + ".dump"
		if prepare:
			self.prepare_dumpfile(filename, dump_file)
		spectrogram = pickle.load(open(dump_file, "rb"))
		self.bars = spectrogram.bars
		self.spectrogram = spectrogram.spectrogram
		self.time_index_ratio = spectrogram.time_index_ratio
		self.frequencies_index_ratio = spectrogram.frequencies_index_ratio

	def prepare_dumpfile(self, filename, dump_file):
		import librosa
		import numpy as np
		time_series, sample_rate = librosa.load(filename)  # getting information from the file

		# getting a matrix which contains amplitude values according to frequency and time indexes
		stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048 * 4))

		self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

		frequencies = librosa.core.fft_frequencies(n_fft=2048 * 4)  # getting an array of frequencies

		# getting an array of time periodic
		frames = np.arange(self.spectrogram.shape[1])
		times = librosa.core.frames_to_time(frames, sr=sample_rate, hop_length=512, n_fft=2048 * 4)
		self.time_index_ratio = len(times) / times[len(times) - 1]
		self.frequencies_index_ratio = len(frequencies) / frequencies[len(frequencies) - 1]
		self.bars = []
		frequencies = np.arange(100, 8000, 200)
		width = 6
		x = 200
		for c in frequencies:
			self.bars.append(AudioBar(x, 100, c, (0, 255, 0), max_height=100, width=width))
			x += width

		pickle.dump(self, open(dump_file, "wb"))

	def get_decibel(self, target_time, freq):
		return self.spectrogram[int(freq * self.frequencies_index_ratio)][int(target_time * self.time_index_ratio)]


class AudioBar:
	def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
		self.x, self.y, self.freq = x, y, freq
		self.color = color
		self.width, self.min_height, self.max_height = width, min_height, max_height
		self.height = min_height
		self.min_decibel, self.max_decibel = min_decibel, max_decibel
		self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

	def update(self, decibel):
		desired_height = decibel * self.__decibel_height_ratio + self.max_height
		self.height = clamp(self.min_height, self.max_height, desired_height)

	def render(self, screen):
		pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.max_height))
		pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))
