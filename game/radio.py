# encoding=utf-8

import game
import pygame

from game.oscilloscope import Oscilloscope


class Radio(game.Entity):
	def __init__(self):
		super(Radio, self).__init__((globals.WIDTH, globals.HEIGHT))
		# set up the mixer
		
		try: pygame.mixer.quit()
		except: pass
		
		freq = 44100	 # audio CD quality
		bitsize = -16	# unsigned 16 bit
		channels = 2	 # 1 is mono, 2 is stereo
		buffer = 2048	# number of samples (experiment to get right sound)
		pygame.mixer.init(freq, bitsize, channels, buffer)
		self.osc = Oscilloscope() 
		self.osc.open(self)
		self.paused = True
		self.loaded = False
		self.spectrum = None 
		self.filename = ""
	
	def play_rnd(self):
		# file = files[randint(0,len(files)-1)]
		# self.filename = file
		# pygame.mixer.music.load(file)
		# self.spectrum = LogSpectrum(file,force_mono=True)
		pygame.mixer.music.play()
		self.loaded = True
		self.paused = False
		
	def play(self):
		if self.loaded:
			self.paused = False
			pygame.mixer.music.unpause()
		else:
			self.play_rnd()
		
	def stop(self):
		self.paused = True
		pygame.mixer.music.pause()

	def update(self, *args, **kwargs):
		super(Radio, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		if not self.paused :
			f,p = None,[0 for i in range(21)]
			start = pygame.mixer.music.get_pos() / 1000.0
			try:
				f,p = self.spectrum.get_mono(start-0.001, start+0.001)
			except:
				pass
			self.osc.update(start*50,f,p)	
		if self.osc:
			self.blit(self.osc.screen, (550, 150))
            
            # metadata = mutagen.File(filename, easy = True)
			
		selectFont = pygame.font.Font('monofonto.ttf', 24)
		basicFont = pygame.font.Font('monofonto.ttf', 22)
        
        # text = selectFont.render(game.Entity.name, True, (105, 251, 187), (0, 0, 0))
        
		#text = selectFont.render(" -   Random Play Radio ", True, (105, 251, 187), (0, 0, 0))
		
        # self.blit(text, (75, 75))
		# text = basicFont.render("  'r' selects a random song ", True, (105, 251, 187), (0, 0, 0))
		# self.blit(text, (75, 100))
		# text = basicFont.render("  'p' to play   's' to stop ", True, (105, 251, 187), (0, 0, 0))
		# self.blit(text, (75, 120))
		
		# if self.filename:
        #     text = selectFont.render(" %s " % metadata["ARTIST"] + ' - ' + metadata["TITLE"], True, (105, 251, 187), (0, 0, 0))
        #
		# 	#text = selectFont.render(u" %s " % self.filename[self.filename.rfind(os.sep)+1:], True, (105, 251, 187), (0, 0, 0))
		# 	self.blit(text, (75, 200))
		#
		# super(Radio, self).update(*args, **kwargs)


# def play_pygame(file):
#
# 	clock = pygame.time.Clock()
# 	# set up the mixer
# 	freq = 44100	 # audio CD quality
# 	bitsize = -16	# unsigned 16 bit
# 	channels = 2	 # 1 is mono, 2 is stereo
# 	buffer = 2048	# number of samples (experiment to get right sound)
# 	pygame.mixer.init(freq, bitsize, channels, buffer)
#
# 	while not pygame.mixer.get_init():
# 		clock.tick(50)
#
# 	pygame.mixer.music.load(file)
# 	osc = Oscilloscope()
# 	osc.open()
#
# 	f = None
# 	p = None
# 	running = True
# 	paused = False
# 	pygame.mixer.music.play()
#
# 	while pygame.mixer.music.get_busy() and running :
# 		if not paused:
# 			start = pygame.mixer.music.get_pos() / 1000.0
# 			# try:
# 			# 	f,p = s.get_mono(start-0.001, start+0.001)
# 			# except:
# 			# 	pass
# 			osc.update(start*50,f,p)
# 		pygame.time.wait(50)
#
# 		for event in pygame.event.get():
# 			if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
# 				if (event.key == pygame.K_UP):
# 					pygame.mixer.music.pause()
# 					paused = True
# 				elif (event.key == pygame.K_DOWN):
# 					pygame.mixer.music.unpause()
# 					paused = False
# 			elif event.type == pygame.QUIT:
# 				running = False
# 	pygame.mixer.quit()
			
if __name__ == "__main__":
	pass
