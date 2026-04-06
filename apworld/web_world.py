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
