from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .jsondata import location_descriptions, item_descriptions
from .options import option_groups


class RingRacersWebWorld(WebWorld):
	game = "Dr. Robotnik's Ring Racers"
	theme = "grassFlowers"
	option_groups = option_groups
	#option_presets = option_presets
	location_descriptions = location_descriptions
	item_descriptions = item_descriptions

	setup_en = Tutorial(
		"Multiworld Setup Guide",
		"A guide to setting up Dr. Robotnik's Ring Racers for MultiWorld.",
		"English",
		"setup_en.md",
		"setup/en",
		["TehRealSalt"],
	)

