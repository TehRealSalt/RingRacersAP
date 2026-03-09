from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

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
    ring_cup = world.get_region("Ring Cup")
    ring_cup.add_event(
        "Ring Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    sneaker_cup = world.get_region("Sneaker Cup")
    sneaker_cup.add_event(
        "Sneaker Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    spring_cup = world.get_region("Spring Cup")
    spring_cup.add_event(
        "Spring Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    barrier_cup = world.get_region("Barrier Cup")
    barrier_cup.add_event(
        "Barrier Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    invincible_cup = world.get_region("Invincible Cup")
    invincible_cup.add_event(
        "Invincible Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    emerald_cup = world.get_region("Emerald Cup")
    emerald_cup.add_event(
        "Emerald Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    extra_cup = world.get_region("Extra Cup")
    extra_cup.add_event(
        "Extra Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    spb_cup = world.get_region("S.P.B. Cup")
    spb_cup.add_event(
        "S.P.B. Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    rocket_cup = world.get_region("Rocket Cup")
    rocket_cup.add_event(
        "Rocket Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    aqua_cup = world.get_region("Aqua Cup")
    aqua_cup.add_event(
        "Aqua Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    lightning_cup = world.get_region("Lightning Cup")
    lightning_cup.add_event(
        "Lightning Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    flame_cup = world.get_region("Flame Cup")
    flame_cup.add_event(
        "Flame Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    super_cup = world.get_region("Super Cup")
    super_cup.add_event(
        "Super Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    egg_cup = world.get_region("Egg Cup")
    egg_cup.add_event(
        "Egg Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    goggles_cup = world.get_region("Goggles Cup")
    goggles_cup.add_event(
        "Goggles Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    timer_cup = world.get_region("Timer Cup")
    timer_cup.add_event(
        "Timer Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    grow_cup = world.get_region("Grow Cup")
    grow_cup.add_event(
        "Grow Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    chao_cup = world.get_region("Chao Cup")
    chao_cup.add_event(
        "Chao Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    wing_cup = world.get_region("Wing Cup")
    wing_cup.add_event(
        "Wing Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    mega_cup = world.get_region("Mega Cup")
    mega_cup.add_event(
        "Mega Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    phantom_cup = world.get_region("Phantom Cup")
    phantom_cup.add_event(
        "Phantom Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    flash_cup = world.get_region("Flash Cup")
    flash_cup.add_event(
        "Flash Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    swap_cup = world.get_region("Swap Cup")
    swap_cup.add_event(
        "Swap Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    shrink_cup = world.get_region("Shrink Cup")
    shrink_cup.add_event(
        "Shrink Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    bomb_cup = world.get_region("Bomb Cup")
    bomb_cup.add_event(
        "Bomb Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    power_cup = world.get_region("Power Cup")
    power_cup.add_event(
        "Power Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    genesis_cup = world.get_region("Genesis Cup")
    genesis_cup.add_event(
        "Genesis Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    skate_cup = world.get_region("Skate Cup")
    skate_cup.add_event(
        "Skate Cup Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    recycle_cup_a = world.get_region("Recycle Cup A")
    recycle_cup_a.add_event(
        "Recycle Cup A Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )

    recycle_cup_b = world.get_region("Recycle Cup B")
    recycle_cup_b.add_event(
        "Recycle Cup B Complete", "Cup Trophy",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )
