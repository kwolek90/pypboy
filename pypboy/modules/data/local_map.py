import pygame
import pypboy
import config
import game
import threading
from pypboy.maps import Maps


class Module(pypboy.SubModule):

	label = "Map"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		map_grid = Map(config.WIDTH, pygame.Rect(4, (config.WIDTH - config.HEIGHT) / 2, config.WIDTH - 8, config.HEIGHT - 80))

		# map_grid.fetch_map(config.MAP_FOCUS, 0.003)
		self.add(map_grid)
		# map_grid.rect[0] = 4
		# map_grid.rect[1] = 40

	def handle_resume(self):
		self.parent.pypboy.header.headline = "DATA"
		self.parent.pypboy.header.title = "Local"
		self.image = pygame.image.load(config.MAP_IMAGE)
		print(self.image)
		super(Module, self).handle_resume()


class Map(game.Entity):
	_mapper = None
	_transposed = None
	_size = 0
	_fetching = None
	_map_surface = None
	_loading_size = 0
	_render_rect = None

	def __init__(self, width, render_rect=None, *args, **kwargs):
		self._mapper = Maps()
		self._size = width
		self._map_surface = pygame.Surface((width, width))
		self._render_rect = render_rect
		super(Map, self).__init__((width, width), *args, **kwargs)
		print(config.MAP_IMAGE)
		self.image = pygame.transform.scale(pygame.image.load(config.MAP_IMAGE), (config.WIDTH - 8, config.HEIGHT - 8))
		#text = config.FONTS[14].render("Loading map...", True, (95, 255, 177), (0, 0, 0))
		#self.image.blit(text, (10, 10))

	def fetch_map(self, position, radius):
		self._fetching = threading.Thread(target=self._internal_fetch_map, args=(position, radius))
		self._fetching.start()

	def _internal_fetch_map(self, position, radius):
		self._mapper.fetch_by_coordinate(position, radius)
		self.redraw_map()

	def update(self, *args, **kwargs):
		super(Map, self).update(*args, **kwargs)
	# 	self.image = pygame.image.load(config.MAP_IMAGE)
	#
	# def render(self, *args, **kwargs):
	# 	self.image = pygame.image.load(config.MAP_IMAGE)

	def move_map(self, x, y):
		self._render_rect.move_ip(x, y)

	def redraw_map(self, coef = 1):
		self._map_surface.fill((0, 0, 0))
		self.image = pygame.image.load(config.MAP_IMAGE)
		# coef_size = self._size / coef
		# for way in self._mapper.transpose_ways((coef_size, coef_size), (self._size / 2, self._size / 2)):
		# 	pygame.draw.lines(
		# 		self._map_surface,
		# 		(85, 251, 167),
		# 		False,
		# 		way,
		# 		2
		# 	)
		# for tag in self._mapper.transpose_tags((coef_size, coef_size), (self._size / 2, self._size / 2)):
		# 	if tag[3] in config.AMENITIES:
		# 		image = config.AMENITIES[tag[3]]
		# 	else:
		# 		print("Unknown amenity: %s" % tag[3])
		# 		image = config.MAP_ICONS['misc']
		# 	pygame.transform.scale(image, (10, 10))
		# 	self._map_surface.blit(image, (tag[1], tag[2]))
		# 	text = config.FONTS[12].render(tag[0], True, (95, 255, 177), (0, 0, 0))
		# 	self._map_surface.blit(text, (tag[1] + 17, tag[2] + 4))

		self.image.blit(self._map_surface, (0, 0), area=self._render_rect)


class MapSquare(game.Entity):
	_mapper = None
	_size = 0
	_fetching = None
	_map_surface = None
	map_position = (0, 0)

	def __init__(self, size, map_position, parent, *args, **kwargs):
		self._mapper = pypboy.maps.Maps()
		self._size = size
		self.parent = parent
		self._map_surface = pygame.Surface((size * 2, size * 2))
		self.map_position = map_position
		self.tags = {}
		super(MapSquare, self).__init__((size, size), *args, **kwargs)

	def fetch_map(self):
		self._fetching = threading.Thread(target=self._internal_fetch_map)
		self._fetching.start()

	def _internal_fetch_map(self):
		self._mapper.fetch_grid(self.map_position)
		self.redraw_map()
		self.parent.redraw_map()

	def redraw_map(self, coef=1):
		self._map_surface.fill((0, 0, 0))
		for way in self._mapper.transpose_ways((self._size, self._size), (self._size / 2, self._size / 2)):
			pygame.draw.lines(
				self._map_surface,
				(85, 251, 167),
				False,
				way,
				1
			)
		for tag in self._mapper.transpose_tags((self._size, self._size), (self._size / 2, self._size / 2)):
			self.tags[tag[0]] = (tag[1] + self.position[0], tag[2] + self.position[1], tag[3])
		self.image.fill((0, 0, 0))
		self.image.blit(self._map_surface, (-self._size / 2, -self._size / 2))


class MapGrid(game.Entity):
	_grid = None
	_delta = 0.002
	_starting_position = (0, 0)

	def __init__(self, starting_position, dimensions, *args, **kwargs):
		self._grid = []
		self._starting_position = starting_position
		self.dimensions = dimensions
		self._tag_surface = pygame.Surface(dimensions)
		super(MapGrid, self).__init__(dimensions, *args, **kwargs)
		self.tags = {}
		self.fetch_outwards()

	def test_fetch(self):
		for x in range(10):
			for y in range(5):
				square = MapSquare(
					100,
					(
						self._starting_position[0] + (self._delta * x),
						self._starting_position[1] - (self._delta * y)
					)
				)
				square.fetch_map()
				square.position = (100 * x, 100 * y)
				self._grid.append(square)

	def fetch_outwards(self):
		for x in range(-4, 4):
			for y in range(-2, 2):
				square = MapSquare(
					86,
					(
						self._starting_position[0] + (self._delta * x),
						self._starting_position[1] - (self._delta * y)
					),
					self
				)
				square.fetch_map()
				square.position = ((86 * x) + (self.dimensions[0] / 2) - 43, (86 * y) + (self.dimensions[1] / 2) - 43)
				self._grid.append(square)

	def draw_tags(self):
		self.tags = {}
		for square in self._grid:
			self.tags.update(square.tags)
		self._tag_surface.fill((0, 0, 0))
		for name in self.tags:
			if self.tags[name][2] in config.AMENITIES:
				image = config.AMENITIES[self.tags[name][2]]
			else:
				print("Unknown amenity: %s" % self.tags[name][2])
				image = config.MAP_ICONS['misc']
			pygame.transform.scale(image, (10, 10))
			self.image.blit(image, (self.tags[name][0], self.tags[name][1]))
			text = config.FONTS[12].render(name, True, (95, 255, 177), (0, 0, 0))
			self.image.blit(text, (self.tags[name][0] + 17, self.tags[name][1] + 4))

	def redraw_map(self, *args, **kwargs):
		self.image.fill((0, 0, 0))
		for square in self._grid:
			self.image.blit(square._map_surface, square.position)
		self.draw_tags()

