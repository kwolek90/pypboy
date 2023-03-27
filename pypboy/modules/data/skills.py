import pypboy
import game
import config


class Module(pypboy.SubModule):

	label = "Skills"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)

		self.skills = []
		self.skills.append(Skill("Naukowiec 3", "Naukowy koksu"))
		self.skills.append(Skill("Genetyk", "Wciąga geny nosem"))
		self.skills.append(Skill("Biochemik", "Bo trzeba badać co ktoś ćpał i to produkować"))
		self.selected_skill = None

		for skill in self.skills:
			self.add(skill)

		handlers = []
		for x in range(len(self.skills)):
			handlers.append(lambda x=x: self.select_skill(x))

		self.menu = pypboy.menu.Menu(250, [x.name for x in self.skills], handlers, 0)
		self.menu.rect[0] = 4
		self.menu.rect[1] = 50

		self.add(self.menu)

	def select_skill(self, skill_idx):
		if self.selected_skill:
			self.selected_skill.clear()
		skill = self.skills[skill_idx]
		print(skill_idx, skill.name)
		skill.print()
		self.selected_skill = skill


class Skill(game.Entity):
	def __init__(self, name, description, *args, **kwargs):
		super(Skill, self).__init__((config.WIDTH, config.HEIGHT), *args, **kwargs)
		self.name = name
		self.text = description

	def render(self, *args, **kwargs):
		pass

	def update(self, *args, **kwargs):
		pass

	def print(self, *args, **kwargs):
		font_size = 8
		line_length = int((config.WIDTH - 150) / (font_size / 2))

		text = ""
		line_idx = 0
		for line in self.text.splitlines():
			for word in line.split():
				if len(word) + len(text) > line_length:
					self.image.blit(config.FONTS[font_size].render(text, True, (105, 255, 187), (0, 0, 0)),
									(140, 50 + line_idx * font_size))
					text = ""
					line_idx += 1
				text += word + " "
			self.image.blit(config.FONTS[font_size].render(text, True, (105, 255, 187), (0, 0, 0)),
							(140, 50 + line_idx * font_size))
			text = ""
			line_idx += 1

	def clear(self):
		self.image.fill((0, 0, 0))