import pygame
import os

VERSION = "0.0.1"

WIDTH = 480
HEIGHT = 320

RADIO_DIRECTORY = os.path.expanduser("~") + "/pypboy_data/radio/"
NOTES_DIRECTORY = os.path.expanduser("~") + "/pypboy_data/notes/"
ICONS_DIRECTORY = os.path.expanduser("~") + "/pypboy_data/icons/"

MAP_FOCUS = (17.28789434494558, 53.52622447868417)

EVENTS = {
	'SONG_END': pygame.USEREVENT + 1
}

ACTIONS = {
	pygame.K_LEFT: "dial_left",
	pygame.K_RIGHT: "dial_right",
	pygame.K_UP: "dial_up",
	pygame.K_DOWN: "dial_down",
	pygame.K_p: "pause",
}

# Using GPIO.BCM as mode
GPIO_ACTIONS = {
	5: "dial_left", #GPIO 27
	6: "dial_right", #GPIO 27
	31: "dial_up", #GPIO 23
	27: "dial_down", #GPIO 7
	26: "pause",  # GPIO 7
}


MAP_ICONS = {
	"camp": 		pygame.image.load('images/map_icons/camp.png'),
	"factory": 		pygame.image.load('images/map_icons/factory.png'),
	"metro": 		pygame.image.load('images/map_icons/metro.png'),
	"misc": 		pygame.image.load('images/map_icons/misc.png'),
	"monument": 	pygame.image.load('images/map_icons/monument.png'),
	"vault": 		pygame.image.load('images/map_icons/vault.png'),
	"settlement": 	pygame.image.load('images/map_icons/settlement.png'),
	"ruin": 		pygame.image.load('images/map_icons/ruin.png'),
	"cave": 		pygame.image.load('images/map_icons/cave.png'),
	"landmark": 	pygame.image.load('images/map_icons/landmark.png'),
	"city": 		pygame.image.load('images/map_icons/city.png'),
	"office": 		pygame.image.load('images/map_icons/office.png'),
	"sewer": 		pygame.image.load('images/map_icons/sewer.png'),
}

AMENITIES = {
	'pub': 				MAP_ICONS['vault'],
	'nightclub': 		MAP_ICONS['vault'],
	'bar': 				MAP_ICONS['vault'],
	'fast_food': 		MAP_ICONS['sewer'],
	'cafe': 			MAP_ICONS['sewer'],
	'drinking_water': 	MAP_ICONS['sewer'],
	'restaurant': 		MAP_ICONS['settlement'],
	'cinema': 			MAP_ICONS['office'],
	'pharmacy': 		MAP_ICONS['office'],
	'school': 			MAP_ICONS['office'],
	'bank': 			MAP_ICONS['monument'],
	'townhall': 		MAP_ICONS['monument'],
	'bicycle_parking': 	MAP_ICONS['misc'],
	'place_of_worship': MAP_ICONS['misc'],
	'theatre': 			MAP_ICONS['misc'],
	'bus_station': 		MAP_ICONS['misc'],
	'parking': 			MAP_ICONS['misc'],
	'fountain': 		MAP_ICONS['misc'],
	'marketplace': 		MAP_ICONS['misc'],
	'atm': 				MAP_ICONS['misc'],
	'university': MAP_ICONS['misc'],
	'clinic': MAP_ICONS['misc'],
}

pygame.font.init()
FONTS = {}
for x in range(8, 28):
	FONTS[x] = pygame.font.Font('monofonto.ttf', x)