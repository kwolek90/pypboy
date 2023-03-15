import numpy
from numpy.fft import fft 
from math import log10
import pygame


class SoundSpectrum:
	""" 
	Obtain the spectrum in a time interval from a sound file. 
	""" 

	left = None 
	right = None 
	
	def __init__(self, filename, force_mono=False): 
		""" 
		Create a new SoundSpectrum instance given the filename of 
		a sound file pygame can read. If the sound is stereo, two 
		spectra are available. Optionally mono can be forced. 
		""" 
		# Get playback frequency 
		nu_play, format, stereo = pygame.mixer.get_init() 
		self.nu_play = 1./nu_play 
		self.format = format 
		self.stereo = stereo 

		# Load sound and convert to array(s) 
		sound = pygame.mixer.Sound(filename)
		a = pygame.sndarray.array(sound) 
		a = numpy.array(a) 
		if stereo: 
			if force_mono: 
				self.stereo = 0 
				self.left = (a[:,0] + a[:,1])*0.5 
			else: 
				self.left = a[:,0] 
				self.right = a[:,1] 
		else: 
			self.left = a 

	def get(self, data, start, stop): 
		""" 
		Return spectrum of given data, between start and stop 
		time in seconds. 
		""" 
		duration = stop-start 
		# Filter data 
		start = int(start/self.nu_play) 
		stop = int(stop/self.nu_play) 
		N = stop - start 
		data = data[start:stop] 

		# Get frequencies 
		frequency = numpy.arange(N/2)/duration 

		# Calculate spectrum 
		spectrum = fft(data)[1:1+N/2] 
		power = (spectrum).real 

		return frequency, power 

	def get_left(self, start, stop): 
		""" 
		Return spectrum of the left stereo channel between 
		start and stop times in seconds. 
		""" 
		return self.get(self.left, start, stop) 

	def get_right(self, start, stop): 
		""" 
		Return spectrum of the left stereo channel between 
		start and stop times in seconds. 
		""" 
		return self.get(self.right, start, stop) 

	def get_mono(self, start, stop): 
		""" 
		Return mono spectrum between start and stop times in seconds. 
		Note: this only works if sound was loaded as mono or mono 
		was forced. 
		""" 
		return self.get(self.left, start, stop) 

class LogSpectrum(SoundSpectrum): 
	""" 
	A SoundSpectrum where the spectrum is divided into 
	logarithmic bins and the logarithm of the power is 
	returned. 
	""" 

	def __init__(self, filename, force_mono=False, bins=20, start=1e2, stop=1e4): 
		""" 
		Create a new LogSpectrum instance given the filename of 
		a sound file pygame can read. If the sound is stereo, two 
		spectra are available. Optionally mono can be forced. 
		The number of spectral bins as well as the frequency range 
		can be specified. 
		""" 
		SoundSpectrum.__init__(self, filename, force_mono=force_mono) 
		start = log10(start) 
		stop = log10(stop) 
		step = (stop - start)/bins 
		self.bins = 10**numpy.arange(start, stop+step, step) 

	def get(self, data, start, stop): 
		""" 
		Return spectrum of given data, between start and stop 
		time in seconds. Spectrum is given as the log of the 
		power in logatithmically equally sized bins. 
		""" 
		f, p = SoundSpectrum.get(self, data, start, stop) 
		bins = self.bins 
		length = len(bins) 
		result = numpy.zeros(length) 
		ind = numpy.searchsorted(bins, f) 
		for i,j in zip(ind, p): 
			if i<length: 
				result[i] += j 
		return bins, result 