import typing
import os, json

from BaseClasses import Item, MultiWorld
from worlds.AutoWorld import World

from . import Items, Locations, Regions
from .Options import RingRacersOptions

client_version = 1

class RingRacersWorld(World):
    """ 
    Dr. Robotnik’s Ring Racers is a Technical Kart Racer, drawing inspiration from anti-grav racers, fighting games, and traditional-style kart racing.
    """

    game: str = "Ring Racers"
    options_dataclass = RingRacersOptions
    options: RingRacersOptions
    topology_present = False

    base_id = 44330000

    item_name_groups = Items.item_groups
    item_name_to_id = Items.item_table
    location_name_to_id = Locations.location_table

    def generate_early(self) -> None:
        if not self.multiworld.get_player_name(self.player).isascii():
            raise Exception("Received Ring Racers yaml with a slot name that has invalid character(s).")

    def fill_slot_data(self) -> dict:
        return {
            "APVersion": 1,
            "PlayerNum": self.player,
        }

    def create_regions(self):
        Regions.create_regions(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        return Items.create_item(name, self.player)

    def create_items(self):
        Items.create_items(self.multiworld, self.player)

    def create_filler(self) -> Item:
        return self.create_item("Nothing")
