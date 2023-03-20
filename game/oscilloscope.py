import copy
import math
import traceback

import numpy
import pygame


class Oscilloscope:

	def __init__(self):
		# Constants
		self.WIDTH, self.HEIGHT = 210, 200
		self.TRACE, self.AFTER, self.GREY = (80, 255, 100),(20, 155, 40),(20, 110, 30)
		self.embedded = False

	def open(self, screen=None):
        # Open window
		pygame.init()
		if screen:
			'''Embedded'''
			self.screen = pygame.Surface((self.WIDTH, self.HEIGHT), 0)
			self.embedded = True
		else:
			'''Own Display'''
			self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0)

		# Create a blank chart with vertical ticks, etc
		self.blank = numpy.zeros((self.WIDTH, self.HEIGHT, 3))
		# Draw x-axis
		self.xaxis = self.HEIGHT/2
		self.blank[::, self.xaxis] = self.GREY
		self.blank[::, self.HEIGHT - 2] = self.TRACE
		self.blank[::, self.HEIGHT - 1] = self.TRACE
		self.blank[::50, self.HEIGHT - 4] = self.TRACE
		self.blank[::50, self.HEIGHT - 3] = self.TRACE
		self.blank[self.WIDTH - 2, ::] = self.TRACE
		self.blank[self.WIDTH - 1, ::] = self.TRACE
		self.blank[self.WIDTH - 3, ::40] = self.TRACE
		self.blank[self.WIDTH - 4, ::40] = self.TRACE

		# Draw vertical ticks
		vticks = [-80, -40, +40, +80]
		for vtick in vticks: self.blank[::5, self.xaxis + vtick] = self.GREY # Horizontals
		for vtick in vticks: self.blank[::50, ::5] = self.GREY			   # Verticals

		# Draw the 'blank' screen.
		pygame.surfarray.blit_array(self.screen, self.blank)	  # Blit the screen buffer
		pygame.display.flip()									 # Flip the double buffer


	def update(self,time,frequency,power):
		try:
			pixels = copy.copy(self.blank)
			offset = 1
			for x in range(self.WIDTH):
				offset = offset - 1
				if offset < -1:
					offset = offset + 1.1
				try:
					pow = power[int(x/10)]
					log = math.log10( pow )
					offset = ((pow / math.pow(10, math.floor(log))) + log)*1.8
				except:
					pass
				try:
					y = float(self.xaxis) - (math.sin((float(x)+float(time))/5.0)*2.0*offset)
					pixels[x][y] = self.TRACE
					pixels[x][y-1] = self.AFTER
					pixels[x][y+1] = self.AFTER
					if abs(y) > 120:
						pixels[x][y-2] = self.AFTER
						pixels[x][y+2] = self.AFTER
				except:
					pass
			pygame.surfarray.blit_array(self.screen, pixels)	 # Blit the screen buffer
			if not self.embedded:
				pygame.display.flip()
		except:
			print(traceback.format_exc())