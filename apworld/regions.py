from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

from . import jsondata

if TYPE_CHECKING:
    from .world import RingRacersWorld


def create_and_connect_regions(world: APQuestWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: APQuestWorld) -> None:
    logging.debug('RingRacers:: Creating regions...')

    menu = Region("Menu", world.player, world.multiworld)
    challenges = Region("Challenge Grid", world.player, world.multiworld)
    cup_select = Region("Cup Select", world.player, world.multiworld)
    lost_n_found = Region("Lost & Found", world.player, world.multiworld)
    tutorial = Region("Tutorial", world.player, world.multiworld)

    regions = [menu, challenges, cup_select, lost_n_found, tutorial]

    for index, cup_def in jsondata.rr_cup_defs.items():
        cup_name = cup_def["label"]
        cup_region = Region(cup_name, world.player, world.multiworld)
        regions.append(cup_region)

    for index, map_def in jsondata.rr_map_defs.items():
        map_name = map_def["label"]
        map_region = Region(map_name, world.player, world.multiworld)
        regions.append(map_region)

    world.multiworld.regions += regions


def connect_regions(world: APQuestWorld) -> None:
    logging.debug('RingRacers:: Connecting regions...')

    menu = world.get_region("Menu")
    challenges = world.get_region("Challenge Grid")
    menu.connect(challenges, "Menu to Challenge Grid")

    cup_select = world.get_region("Cup Select")
    menu.connect(cup_select, "Menu to Cup Select")

    # Connect cups to menu, and then the cup's levels to the cup
    for index, cup_def in jsondata.rr_cup_defs.items():
        cup_name = cup_def["label"]
        cup_region = world.get_region(cup_name)

        cup_entrance_name = "Cup Select to " + cup_name
        cup_select.connect(cup_region, cup_entrance_name)

        for map_index in cup_def["map_list"]:
            map_def = jsondata.rr_map_defs[map_index]
            map_name = map_def["label"]

            map_region = world.get_region(map_name)
            map_entrance_name = cup_name + " to " + map_name
            cup_region.connect(map_region, map_entrance_name)

    # Tutorial + Lost & Found connections
    tutorial_region = world.get_region("Tutorial")
    menu.connect(tutorial_region, "Menu to Tutorial")

    lost_n_found_region = world.get_region("Lost & Found")
    cup_select.connect(lost_n_found_region, "Cup Select to Lost & Found")

    for index, map_def in jsondata.rr_map_defs.items():
        if map_def["type"] == "tutorial":
            map_name = map_def["label"]
            map_region = world.get_region(map_name)
            tutorial_region.connect(map_region, "Tutorial to " + map_name)
        elif map_def.get("item", None):
            map_name = map_def["label"]
            map_region = world.get_region(map_name)
            lost_n_found_region.connect(map_region, "Lost & Found to " + map_name)

    # Handle extra special cases
    sunbeam_controls_region = world.get_region("Sunbeam Paradise: Controls")
    sunbeam_rings_region = world.get_region("Sunbeam Paradise: Rings")
    sunbeam_controls_region.connect(sunbeam_rings_region, "Sunbeam Paradise: Controls to Sunbeam Paradise: Rings")

    test_track_region = world.get_region("Test Track")
    sunbeam_controls_region.connect(test_track_region, "Sunbeam Paradise: Controls to Test Track")

    mystic_cave_region = world.get_region("Mystic Cave")
    hidden_palace_region = world.get_region("Hidden Palace")
    mystic_cave_region.connect(hidden_palace_region, "Mystic Cave to Hidden Palace")

    espresso_lane_region = world.get_region("Espresso Lane")
    adventure_example_region = world.get_region("Adventure Example")
    espresso_lane_region.connect(adventure_example_region, "Espresso Lane to Adventure Example")

    virutal_highway_region = world.get_region("Virtual Highway")
    route_1980_region = world.get_region("Route 1980")
    virutal_highway_region.connect(route_1980_region, "Virtual Highway to Route 1980")
