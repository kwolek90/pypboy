from pypboy import BaseModule
from pypboy.modules.data import local_map
from pypboy.modules.data import status
from pypboy.modules.data import notes
from pypboy.modules.data import items
from pypboy.modules.data import skills
from pypboy.modules.data import radio


class Module(BaseModule):

	label = "DATA"
	GPIO_LED_ID = 21

	def __init__(self, *args, **kwargs):
		self.submodules = [
			status.Module(self),
			skills.Module(self),
			items.Module(self),
			notes.Module(self),
			local_map.Module(self),
			radio.Module(self)
		]
		super(Module, self).__init__(*args, **kwargs)
