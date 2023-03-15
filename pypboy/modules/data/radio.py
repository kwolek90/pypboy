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

		self.select_station(0)

	def select_station(self, station):
		if hasattr(self, 'active_station') and self.active_station:
			self.active_station.stop()
		self.active_station = self.stations[station]
		self.active_station.play_random()


	def handle_event(self, event):
		if event.type == config.EVENTS['SONG_END']:
			if hasattr(self, 'active_station') and self.active_station:
				self.active_station.play_random()