from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import locations, jsondata

if TYPE_CHECKING:
    from .world import RingRacersWorld

class RingRacersItem(Item):
    game = "Dr. Robotnik's Ring Racers"


def get_random_filler_item_name(world: RingRacersWorld) -> str:
    return "KKD Honor"


def create_rr_item(world: RingRacersWorld, name: str) -> RingRacersItem:
    item_def = jsondata.rr_item_defs[name]
    class_str = item_def["class"]
    classification = ItemClassification[class_str]
    return RingRacersItem(name, classification, world.item_name_to_id[name], world.player)


ENGINE_CLASS_LIST = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I"
]

CHALLENGE_FOLLOWERS = [
    "Follower: Tornado",
    "Follower: Chao",
    "Follower: Chao Egg",
    "Follower: Froggy",
    "Follower: Has Bean",
]

def create_all_items(world: RingRacersWorld) -> None:
    logging.debug('RingRacers:: Creating items...')

    item_pool: list[Item] = []
    filler_pool: list[Item] = []

    def group_percent_to_count(requirement: int, group_name: str) -> int:
        total = world.item_name_groups[group_name]
        return (requirement * total + 99) // 100

    #
    # Get starting driver(s)
    #
    starting_driver_pool: list[Item] = []

    def create_driver_item(driver_name: str) -> Item:
        driver_item = world.create_item(driver_name)

        # TODO: Only mark drivers as progression if the specific locations are enabled
        driver_item.classification = ItemClassification.progression_skip_balancing

        return driver_item

    match world.options.starting_driver_pool.value:
        case 0:
            for driver_name in world.item_name_groups["Drivers"]:
                if driver_name in world.item_name_groups["Starting Drivers"]:
                    starting_driver_pool.append(create_driver_item(driver_name))
                else:
                    item_pool.append(create_driver_item(driver_name))
        case 1:
            engine_lists: dict[str, list[Item]] = {}
            for engine in ENGINE_CLASS_LIST:
                engine_lists[engine] = []

                for driver_name in world.item_name_groups["Engine Class {}".format(engine)]:
                    engine_lists[engine].append(create_driver_item(driver_name))

                engine_driver_item = engine_lists[engine].pop(world.random.randrange(len(engine_lists[engine])))
                starting_driver_pool.append(engine_driver_item)
                item_pool += engine_lists[engine]

            # nab the weirdos
            for driver_name in world.item_name_groups["Engine Class J"]:
                item_pool.append(create_driver_item(driver_name))

            for driver_name in world.item_name_groups["Engine Class R"]:
                item_pool.append(create_driver_item(driver_name))

        case _:
            for driver_name in world.item_name_groups["Drivers"]:
                starting_driver_pool.append(create_driver_item(driver_name))

    for i in range(world.options.starting_driver_count.value):
        precollect_driver = starting_driver_pool.pop(world.random.randrange(len(starting_driver_pool)))
        world.push_precollected(precollect_driver)

    # add whatever we didn't use
    item_pool += starting_driver_pool

    #
    # Get starting cup
    #
    starting_cup_pool: list[Item] = []

    for cup_name in world.item_name_groups["Cups"]:
        starting_cup_pool.append(world.create_item(cup_name))

    precollect_cup = starting_cup_pool.pop(world.random.randrange(len(starting_cup_pool)))

    if locations.location_name_allowed(world, "Challenge - Ring Cup"):
        # If challenges are enabled, put our precollected cup there
        starting_cup_location = world.get_location("Challenge - Ring Cup")
        starting_cup_location.place_locked_item(precollect_cup)
    else:
        # Otherwise, just start with it
        world.push_precollected(precollect_cup)

    # add whatever we didn't use
    item_pool += starting_cup_pool

    #
    # Handle followers
    #
    for follower_name in world.item_name_groups["Followers"]:
        follower_item = world.create_item(follower_name)

        # TODO: Only mark followers as progression if the specific locations are enabled
        if follower_name in CHALLENGE_FOLLOWERS:
            follower_item.classification = ItemClassification.progression_deprioritized_skip_balancing
            item_pool.append(follower_item)
        else:
            filler_pool.append(follower_item)

    #
    # Handle colors for Gum's challenge
    #
    color_pool: list[Item] = []
    for color_name in world.item_name_groups["Spray Cans"]:
        color_pool.append(world.create_item(color_name)) 

    if locations.location_name_allowed(world, "Challenge - Driver: Gum"):
        required_percent = group_percent_to_count(75, "Spray Cans")
        for i in range(required_percent):
            prog_color = color_pool.pop(world.random.randrange(len(color_pool)))
            prog_color.classification = ItemClassification.progression_deprioritized_skip_balancing
            item_pool += prog_color

    # remainder stays filler
    filler_pool += color_pool

    #
    # Handle music for Sound Test's challenge
    #
    music_pool: list[Item] = []
    for music_name in world.item_name_groups["Alt. Music"]:
        music_pool.append(world.create_item(music_name)) 

    if locations.location_name_allowed(world, "Challenge - Sound Test"):
        required_percent = group_percent_to_count(25, "Alt. Music")
        for i in range(required_percent):
            prog_music = music_pool.pop(world.random.randrange(len(music_pool)))
            prog_music.classification = ItemClassification.progression_deprioritized_skip_balancing
            item_pool += prog_music

    # remainder stays filler
    filler_pool += music_pool

    #
    # Add some more generic items
    #
    for map_name in world.item_name_groups["Maps"]:
        map_item = world.create_item(map_name)
        if map_item.classification & ItemClassification.progression:
            item_pool.append(map_item)
        else:
            filler_pool.append(map_item)

    for extra_name in world.item_name_groups["Extras"]:
        extra_item = world.create_item(extra_name)
        if extra_item.classification & ItemClassification.progression:
            item_pool.append(extra_item)
        else:
            filler_pool.append(extra_item)

    #
    # Determine how much filler is needed
    #
    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    
    existing_number_of_filler_items = len(filler_pool)
    if needed_number_of_filler_items > existing_number_of_filler_items:
        needed_new_filler = needed_number_of_filler_items - existing_number_of_filler_items
        filler_pool += [world.create_filler() for _ in range(needed_new_filler)]

    if needed_number_of_filler_items == len(filler_pool):
        # just slam it in if it's the right size!
        item_pool += filler_pool
    else:
        for _ in range(needed_number_of_filler_items):
            item_pool.append(filler_pool.pop(world.random.randrange(len(filler_pool))))

    # Commit to the multiworld
    world.multiworld.itempool += item_pool
