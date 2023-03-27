import pypboy
import game
import os
import config


class Module(pypboy.SubModule):

	label = "Notes"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		self.notes = [Note(config.NOTES_DIRECTORY + x) for x in os.listdir(config.NOTES_DIRECTORY)]
		self.selected_note = None

		for note in self.notes:
			self.add(note)

		handlers = []
		for x in range(len(self.notes)):
			handlers.append(lambda x=x: self.select_note(x))

		self.menu = pypboy.menu.Menu(250, [x.name for x in self.notes], handlers, 0)
		self.menu.rect[0] = 4
		self.menu.rect[1] = 50

		self.add(self.menu)

		self.select_note(0)

	def select_note(self, note_idx):
		if self.selected_note:
			self.selected_note.clear()
		note = self.notes[note_idx]
		print(note_idx, note.name)
		note.print()
		self.selected_note = note


class Note(game.Entity):
	def __init__(self, file, *args, **kwargs):
		super(Note, self).__init__((config.WIDTH, config.HEIGHT), *args, **kwargs)
		text = open(file, encoding="utf8").readlines()
		self.name = text[0][:-1]
		self.text = "".join(text[1:])

	def render(self, *args, **kwargs):
		pass

	def update(self, *args, **kwargs):
		pass

	def print(self, *args, **kwargs):
		font_size = 8
		line_length = int((config.WIDTH-150) / (font_size / 2))

		text = ""
		line_idx = 0
		for line in self.text.splitlines():
			for word in line.split():
				if len(word)+len(text) > line_length:
					self.image.blit(config.FONTS[font_size].render(text, True, (105, 255, 187), (0, 0, 0)), (140, 50+line_idx*font_size))
					text = ""
					line_idx += 1
				text += word + " "
			self.image.blit(config.FONTS[font_size].render(text, True, (105, 255, 187), (0, 0, 0)),	(140, 50 + line_idx * font_size))
			text = ""
			line_idx += 1

	def clear(self):
		self.image.fill((0, 0, 0))

