from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import RingRacersWorld

CHALLENGE_FOLLOWERS = [
    "Follower: Tornado",
    "Follower: Chao",
    "Follower: Chao Egg",
    "Follower: Froggy",
    "Follower: Has Bean",
]

class RingRacersItem(Item):
    game = "Dr. Robotnik's Ring Racers"


def get_random_filler_item_name(world: RingRacersWorld) -> str:
    return "KKD Honor"


def create_rr_item(world: RingRacersWorld, name: str) -> RingRacersItem:
    classification = ItemClassification.filler

    if name == "Follower: Mystic Melody":
        classification = ItemClassification.progression
    elif name in CHALLENGE_FOLLOWERS:
        # Only mark followers that are required for challenges as progression
        classification = ItemClassification.progression_deprioritized_skip_balancing
    elif name in world.item_name_groups["Spray Cans"]:
        # Progression by technicality, because of Gum's Challenge
        classification = ItemClassification.progression_deprioritized_skip_balancing
    elif name in world.item_name_groups["Alt. Music"]:
        # Progression by technicality, because of Sound Test's Challenge
        classification = ItemClassification.progression_deprioritized_skip_balancing
    elif name in world.item_name_groups["Drivers"]:
        # There's probably 1 or 2 drivers that aren't required for challenges,
        # but the vast majority of them are, so just mark them all as progression
        # and be done with it LOL
        classification = ItemClassification.progression_skip_balancing | ItemClassification.useful
    elif (name in world.item_name_groups["Cups"]
        or name in world.item_name_groups["Maps"]
        or name in world.item_name_groups["Extras"]): # TODO: disambiguate
        classification = ItemClassification.progression

    return RingRacersItem(name, classification, world.item_name_to_id[name], world.player)


def create_all_items(world: RingRacersWorld) -> None:
    logging.debug('RingRacers:: Creating items...')

    driver_pool: list[Item] = []

    for driver_name in world.item_name_groups["Drivers"]:
        driver_pool.append(world.create_item(driver_name))

    # TODO: Option for starting driver count
    # TODO: Option for starting driver distribution (vanilla, random, or random-balanced)
    for i in range(9):
        precollect_driver = driver_pool.pop(world.random.randrange(len(driver_pool)))
        world.push_precollected(precollect_driver)

    cup_pool: list[Item] = []

    for cup_name in world.item_name_groups["Cups"]:
        cup_pool.append(world.create_item(cup_name))

    precollect_cup = cup_pool.pop(world.random.randrange(len(cup_pool)))

    # TODO: Putting it on Ring Cup challenge I think is the coolest option
    # for when cup challenges are available, but this will break when
    # the different challenge categories are made into options. Probably
    # just add to starting inventory in this case. 
    starting_cup_location = world.get_location("Challenge - Ring Cup")
    starting_cup_location.place_locked_item(precollect_cup)

    color_pool: list[Item] = []
    for color_name in world.item_name_groups["Spray Cans"]:
        color_pool.append(world.create_item(color_name)) 

    #num_spray_cans_left = len(world.location_name_groups["Spray Cans"]) - len(color_pool)
    #for _ in range(num_spray_cans_left):
    #    color_pool.append(world.create_item("KKD Honor"))
    #logging.debug('RingRacers:: Created {} filler honors'.format(num_spray_cans_left))

    item_pool: list[Item] = []
    item_pool += driver_pool
    item_pool += cup_pool
    item_pool += color_pool

    for follower_name in world.item_name_groups["Followers"]:
        item_pool.append(world.create_item(follower_name))

    for map_name in world.item_name_groups["Maps"]:
        item_pool.append(world.create_item(map_name))

    for extra_name in world.item_name_groups["Extras"]:
        item_pool.append(world.create_item(extra_name))

    for music_name in world.item_name_groups["Alt. Music"]:
        item_pool.append(world.create_item(music_name))

    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items < 0:
        # TEMP: more items than locations SHOULD be an error condition,
        # but I'm hacking things together for a playable prototype for now
        precollect_items = -needed_number_of_filler_items
        for _ in range(precollect_items):
            precollect = item_pool.pop(world.random.randrange(len(item_pool)))
            world.push_precollected(precollect)

        number_of_items = len(item_pool)
        needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
        assert(needed_number_of_filler_items == 0)

    item_pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += item_pool
