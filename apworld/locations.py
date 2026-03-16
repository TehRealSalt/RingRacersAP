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

    # TODO: Actually filter down to just challenges
    all_challenge_locations = get_location_names_with_ids(world, list(world.location_name_to_id.keys()))
    challenges.add_locations(all_challenge_locations, RingRacersLocation)


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
        if map_def["type"] == "special":
            map_name = map_def["label"]
            map_region = world.get_region(map_name)
            event_name = "!" + map_name + " Reachable"

            map_region.add_event(
                event_name, "!Sealed Star Reachable",
                location_type=RingRacersLocation, item_type=items.RingRacersItem
            )


