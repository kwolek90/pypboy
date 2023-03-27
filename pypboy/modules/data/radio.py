import os

import pypboy
import config

from pypboy.modules.data.radio_station import RadioStation


class Module(pypboy.SubModule):

	label = "Radio"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		self.stations = [RadioStation(config.RADIO_DIRECTORY + x + "/") for x in os.listdir(config.RADIO_DIRECTORY)]
		for station in self.stations:
			self.add(station)
		self.active_station = None
		config.radio = self

		handlers = []
		for x in range(len(self.stations)):
			handlers.append(lambda x=x: self.select_station(x))

		self.menu = pypboy.menu.Menu(250, [x.name for x in self.stations], handlers, 0)
		self.menu.rect[0] = 4
		self.menu.rect[1] = 50

		self.add(self.menu)

	def select_station(self, station):
		print(station, self.stations[station].name)
		if hasattr(self, 'active_station') and self.active_station:
			self.active_station.stop()
		self.active_station = self.stations[station]
		self.active_station.play_random()


	def handle_event(self, event):
		if event.type == config.EVENTS['SONG_END']:
			if hasattr(self, 'active_station') and self.active_station:
				self.active_station.play_random()