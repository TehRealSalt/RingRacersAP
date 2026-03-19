from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items, jsondata

if TYPE_CHECKING:
    from .world import RingRacersWorld


class RingRacersLocation(Location):
    game = "Dr. Robotnik's Ring Racers"


def get_location_names_with_ids(world: RingRacersWorld, location_names: list[str]) -> dict[str, int | None]:
    return { location_name: world.location_name_to_id[location_name] for location_name in location_names }


def create_all_locations(world: RingRacersWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: RingRacersWorld) -> None:
    challenges = world.get_region("Challenge Grid")

    all_challenge_locations = get_location_names_with_ids(world, world.location_name_groups["Challenges"])
    challenges.add_locations(all_challenge_locations, RingRacersLocation)

    for index, map_def in jsondata.rr_map_defs.items():
        location_suffix_list = map_def.get("locations", None)
        if location_suffix_list:
            map_name = map_def["label"]
            map_region = world.get_region(map_name)
            map_location_names = map_def["locations"]
            if len(map_location_names):
                all_map_locations = get_location_names_with_ids(world, map_location_names)
                map_region.add_locations(all_map_locations)


def create_events(world: RingRacersWorld) -> None:
    for index, cup_def in jsondata.rr_cup_defs.items():
        cup_name = cup_def["label"]
        cup_region = world.get_region(cup_name)
        event_name = "!" + cup_name + " Reachable"

        cup_region.add_event(
            event_name, "!Cup Trophy",
            location_type=RingRacersLocation, item_type=items.RingRacersItem
        )

    for index, map_def in jsondata.rr_map_defs.items():
        map_name = map_def["label"]
        map_region = world.get_region(map_name)

        time_medal_count = map_def.get("medals_time", 0)
        for i in range(time_medal_count):
            event_name = "!" + map_name + " - Time Medal"
            if time_medal_count > 1:
                event_name += " " + str(i + 1)

            map_region.add_event(
                event_name, "!Medal",
                rule=lambda state: state.has("Time Attack Mode", world.player),
                location_type=RingRacersLocation, item_type=items.RingRacersItem
            )

        spb_medal_count = map_def.get("medals_spb", 0)
        for i in range(spb_medal_count):
            event_name = "!" + map_name + " - SPB Medal"
            if spb_medal_count > 1:
                event_name += " " + str(i + 1)

            map_region.add_event(
                event_name, "!Medal",
                rule=lambda state: state.has("SPB Attack Mode", world.player),
                location_type=RingRacersLocation, item_type=items.RingRacersItem
            )

        prison_medal_count = map_def.get("medals_prisons", 0)
        for i in range(prison_medal_count):
            event_name = "!" + map_name + " - Prisons Medal"
            if prison_medal_count > 1:
                event_name += " " + str(i + 1)

            map_region.add_event(
                event_name, "!Medal",
                rule=lambda state: state.has("Prison Break Mode", world.player),
                location_type=RingRacersLocation, item_type=items.RingRacersItem
            )

        if map_def["type"] == "special":
            event_name = "!" + map_name + " Reachable"
            map_region.add_event(
                event_name, "!Sealed Star Reachable",
                location_type=RingRacersLocation, item_type=items.RingRacersItem
            )


