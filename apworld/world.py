from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World
from Utils import visualize_regions

from . import items, locations, regions, rules, jsondata
from . import options as rr_options

jsondata.load_all()

class RingRacersWorld(World):
    """
    "Dr. Robotnik’s Ring Racers" is a Technical Kart Racer, drawing inspiration from "antigrav" racers,
    fighting games, and traditional-style kart racing.
    """

    game = "Dr. Robotnik's Ring Racers"

    # web = web_world.RingRacersWebWorld

    options_dataclass = rr_options.RingRacersOptions
    options: rr_options.RingRacersOptions

    location_name_to_id = jsondata.location_name_to_id
    item_name_to_id = jsondata.item_name_to_id

    location_name_groups = jsondata.location_name_groups
    item_name_groups = jsondata.item_name_groups

    origin_region_name = "Menu"
    topology_present = True


    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)


    def set_rules(self) -> None:
        rules.set_all_rules(self)


    def create_items(self) -> None:
        items.create_all_items(self)


    def create_item(self, name: str) -> items.RingRacersItem:
        return items.create_rr_item(self, name)


    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)


    def fill_slot_data(self) -> dict:
        return {
            "APVersion": 1,
            "PlayerNum": self.player,
        }
