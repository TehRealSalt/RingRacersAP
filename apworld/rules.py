from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, LocationProgressType
from worlds.generic.Rules import add_rule, set_rule

from . import regions, locations, items, jsondata

if TYPE_CHECKING:
    from .world import RingRacersWorld


def map_mystic_melody(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("Follower: Mystic Melody", player)
        and state.can_reach_region(map_name, player)
    )


def map_time_attack(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("Time Attack Mode", player)
        and state.can_reach_region(map_name, player)
    )


def map_prison_break(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("Prison Break Mode", player)
        and state.can_reach_region(map_name, player)
    )


def map_spb_attack(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("SPB Attack Mode", player)
        and state.can_reach_region(map_name, player)
    )


def can_reach_sealed_star(state: CollectionState, player: int) -> bool:
    return state.has("!Sealed Star Reachable", player)


def have_all_cups(state: CollectionState, player: int) -> bool:
    return state.has_all(state.multiworld.worlds[player].item_name_groups["Cups"], player)


def have_all_maps_but_test_run(state: CollectionState, player: int) -> bool:
    all_access_items = []
    all_access_items += list(state.multiworld.worlds[player].item_name_groups["Cups"])
    all_access_items += list(state.multiworld.worlds[player].item_name_groups["Maps"])
    all_access_items.remove("Test Run Access")
    return state.has_all(all_access_items, player)


def can_reach_chaos_emeralds(state: CollectionState, player: int) -> bool:
    # TODO: Is there any case where we need to check reachability of the Sealed Stars themselves?
    return state.has_all((
        "Ring Cup Access",
        "Sneaker Cup Access",
        "Spring Cup Access",
        "Barrier Cup Access",
        "Invincible Cup Access",
        "Emerald Cup Access",
        "Extra Cup Access"
    ), player)


def can_reach_all_emeralds(state: CollectionState, player: int) -> bool:
    # TODO: Is there any case where we need to check reachability of the Sealed Stars themselves?
    return state.has_all((
        "Ring Cup Access",
        "Sneaker Cup Access",
        "Spring Cup Access",
        "Barrier Cup Access",
        "Invincible Cup Access",
        "Emerald Cup Access",
        "Extra Cup Access",
        "S.P.B. Cup Access",
        "Rocket Cup Access",
        "Aqua Cup Access",
        "Lightning Cup Access",
        "Flame Cup Access",
        "Super Cup Access",
        "Egg Cup Access"
    ), player)


def have_vicious_mode(state: CollectionState, player: int) -> bool:
    return (
        state.has("Gear 3 + GP Vicious Mode", player)
        or state.has("Progressive Difficulty", player, 1)
    )


def have_master_mode(state: CollectionState, player: int) -> bool:
    return (
        state.has_all(("Gear 3 + GP Vicious Mode", "GP Master Mode"), player) # Menu flow requires Vicious accessible too
        or state.has("Progressive Difficulty", player, 2)
    )


def enough_medals(state: CollectionState, count: int, player: int) -> bool:
    return state.has("!Medal", player, count)


def have_all_guest_drivers(state: CollectionState, player: int) -> bool:
    # Not including Trouble Bruin is intentional, but keep an
    # eye on if the main game fixes this issue
    return state.has_all(( 
        "Driver: AiAi",
        "Driver: Aigis",
        "Driver: Arle",
        "Driver: Azusa Miura",
        "Driver: Billy Hatcher",
        "Driver: Carol",
        "Driver: Chuchu",
        "Driver: Ecco",
        "Driver: Gum",
        "Driver: Headdy",
        "Driver: Jack Frost",
        "Driver: Mail",
        "Driver: NiGHTS",
        "Driver: Orta",
        "Driver: Pulseman",
        "Driver: Rappy",
        "Driver: Sakura Shinguji",
        "Driver: Vectorman",
        "Driver: Wonder Boy"
    ), player)


def have_group_percentage(state: CollectionState, group: str, player: int, requirement: int) -> bool:
    unlocked = state.count_group(group, player)
    total = len(state.multiworld.worlds[player].item_name_groups[group])
    return (100 * unlocked) >= (total * requirement)


def set_all_rules(world: RingRacersWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: RingRacersWorld) -> None:
    logging.debug('RingRacers:: Setting entrance rules...')

    for index, cup_def in jsondata.rr_cup_defs.items():
        access_item = cup_def.get("item", None)
        if access_item:
            cup_entrance_name = "Cup Select to " + cup_def["label"]
            set_rule(
                world.get_entrance(cup_entrance_name),
                lambda state, item=access_item:
                    state.has(item, world.player)
            )

    for index, map_def in jsondata.rr_map_defs.items():
        access_item = map_def.get("item", None)
        if access_item:
            if map_def["type"] == "tutorial":
                map_entrance_name = "Tutorial to " + map_def["label"]
            elif map_def.get("item", None):
                map_entrance_name = "Lost & Found to " + map_def["label"]
            else:
                continue

            map_entrance = world.get_entrance(map_entrance_name)
            set_rule(
                map_entrance,
                lambda state, item=access_item:
                    state.has(item, world.player)
            )

            if (world.options.simple_map_access
            and not map_def.get("no_visit_needed", False)):
                add_rule(
                    map_entrance,
                    lambda state, region=map_def["label"]:
                        state.can_reach_region(region, world.player)
                )


def set_driver_challenge_location_rules(world: RingRacersWorld) -> None:
    set_rule(
        world.get_location("Challenge - Driver: AiAi"),
        lambda state:
            have_vicious_mode(state, world.player)
            and state.can_reach_region("Monkey Mall", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Aigis"),
        lambda state:
            state.can_reach_region("Operator's Overspace", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Azusa Miura"),
        lambda state:
            (state.has("Driver: Honey", world.player) and state.can_reach_region("765 Stadium", world.player))
            or map_mystic_melody(state, "765 Stadium", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Arle"),
        lambda state:
            map_mystic_melody(state, "Melty Manor", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Bark"),
        lambda state:
            map_time_attack(state, "Sub-Zero Peak", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Battle Kukku XV"),
        lambda state:
            map_time_attack(state, "Vermilion Vessel", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Bean"),
        lambda state:
            state.can_reach_region("Tinkerer's Arena", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Big"),
        lambda state:
            state.can_reach_region("Emerald Coast", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Billy Hatcher"),
        lambda state:
            state.can_reach_region("Joypolis", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Blaze"),
        lambda state:
            map_time_attack(state, "Blizzard Peaks", world.player)
    )

    #
    # "Challenge - Driver: Bomb" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Driver: Carol"),
        lambda state:
            state.can_reach_region("Aqua Tunnel", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Caterkiller"),
        lambda state:
            state.has("Driver: Dr. Eggman", world.player) and state.can_reach_region("Desert Palace", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Chao"),
        lambda state:
            state.has("Follower: Chao Egg", world.player)
            or map_mystic_melody(state, "City Escape", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Chaos Zero"),
        lambda state:
            state.has("Driver: Sonic", world.player)
            and can_reach_sealed_star(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Charmy"),
        lambda state:
            map_time_attack(state, "Isolated Island", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Chuchu"),
        lambda state:
            state.can_reach_region("Neon Resort", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Cluckoid"),
        lambda state:
            state.can_reach_region("Tree Ring", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Cream"),
        lambda state:
            state.has("Driver: Blaze", world.player)
            and state.can_reach_region("Leaf Storm", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Ecco"),
        lambda state:
            state.can_reach_region("Azure Axiom", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Eggrobo"),
        lambda state:
            state.has("Driver: Knuckles", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Emerl"),
        lambda state:
            state.can_reach_region("Tails' Lab", world.player)
    )

    #
    # "Challenge - Driver: Espio" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Driver: Flicky"),
        lambda state:
            state.has("Driver: Motobug", world.player)
    )

    if locations.location_name_allowed(world, "Challenge - Driver: Gum"):
        gum_location = world.get_location("Challenge - Driver: Gum")
        set_rule(
            gum_location,
            lambda state:
                have_group_percentage(state, "Spray Cans", world.player, 75)
        )
        # Requires over 50% of colors, exclude
        gum_location.progress_type = LocationProgressType.EXCLUDED

    set_rule(
        world.get_location("Challenge - Driver: Gutbuster"),
        lambda state:
            state.has_all(("Driver: Bomb", "Driver: Heavy"), world.player)
            and map_time_attack(state, "Sundae Drive", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Headdy"),
        lambda state:
            map_mystic_melody(state, "Northern District", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Heavy"),
        lambda state:
            map_prison_break(state, "Electra Clacker", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Heavy Magician"),
        lambda state:
            have_group_percentage(state, "Drivers", world.player, 50)
    )

    set_rule(
        world.get_location("Challenge - Driver: Honey"),
        lambda state:
            state.can_reach_region("Death Egg's Eye", world.player)
            #or map_time_attack(state, "Death Egg's Eye", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Jack Frost"),
        lambda state:
            state.can_reach_region("SRB2 Frozen Night", world.player)
            # Technically always possible to crash the game,
            # but we probably don't want that in logic.
    )

    set_rule(
        world.get_location("Challenge - Driver: Jet"),
        lambda state:
            state.can_reach_region("Sky Babylon", world.player)
    )

    #
    # "Challenge - Driver: Orenzo"
    #

    #
    # "Challenge - Driver: Mail" is always possible by technicality,
    # but we don't want to expect people to get this logically by
    # standing inside of of the infinite ring machine for 2 million
    # years. Requirement was nerfed to 9999, and expect enough cups
    # to be unlocked to get it naturally. My math is that 200 rings
    # is on the low end of what you can get in a regular race. So,
    # we need to be able to finish 50 race maps, which means we
    # need access to 10 cups.
    #
    set_rule(
        world.get_location("Challenge - Driver: Mail"),
        lambda state:
            state.has_group("Cups", world.player, 10)
    )

    set_rule(
        world.get_location("Challenge - Driver: Maria"),
        lambda state:
            map_mystic_melody(state, "Lost Colony", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Mecha Sonic"),
        lambda state:
            state.has("Driver: Knuckles", world.player)
            and have_vicious_mode(state, world.player)
            and state.can_reach_region("Sky Sanctuary", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Metal Knuckles"),
        lambda state:
            state.has("Driver: Tails Doll", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: NiGHTS"),
        lambda state:
            map_mystic_melody(state, "Avant Garden", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Orta"),
        lambda state:
            can_reach_sealed_star(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Pulseman"),
        lambda state:
            state.can_reach_region("Kodachrome Void", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Rappy"),
        lambda state:
            state.can_reach_region("Las Vegas", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Ray"),
        lambda state:
            state.has("Driver: Mighty", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Redz"),
        lambda state:
            state.can_reach_region("Hidden Palace", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Rouge"),
        lambda state:
            # Technically possible in Free Play, but it's inconvenient
            # to access as a single player, so require Prison Break.
            map_prison_break(state, "Security Hall", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Sakura Shinguji"),
        lambda state:
            state.can_reach_region("Hanagumi Hall", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Shadow"),
        lambda state:
            state.can_reach_region("Lost Colony", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Silver"),
        lambda state:
            state.can_reach_region("Mega Collision Chaos", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Surge"),
        lambda state:
            map_mystic_melody(state, "Emerald Hill", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Tails Doll"),
        lambda state:
            map_mystic_melody(state, "Regal Ruin", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Tikal"),
        lambda state:
            map_mystic_melody(state, "Coastal Temple", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Vectorman"),
        lambda state:
            state.can_reach_region("Dark Fortress", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Whisper"),
        lambda state:
            state.can_reach_region("Withering Chateau", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Wonder Boy"),
        lambda state:
            map_mystic_melody(state, "Darkvile Castle 2", world.player)
    )

    set_rule(
        world.get_location("Challenge - Driver: Zipp"),
        lambda state:
            map_mystic_melody(state, "Hidden Palace", world.player)
    )

    ring_the_racer_location = world.get_location("Challenge - Driver: Ring the Racer")
    set_rule(
        ring_the_racer_location,
        lambda state:
            state.has("Driver: Mail", world.player)
            and state.can_reach_region("Sunbeam Paradise: Controls", world.player)
    )
    ring_the_racer_location.progress_type = LocationProgressType.EXCLUDED

    set_rule(
        world.get_location("Challenge - Driver: Trouble Bruin"),
        lambda state:
            state.has("Driver: Headdy", world.player)
            and have_vicious_mode(state, world.player)
            and state.can_reach_region("Trap Tower", world.player)
    )

    # Only include the character wins in logic if we nerf them
    if world.options.character_wins_count > 0:
        add_rule(
            world.get_location("Challenge - Driver: Bark"),
            lambda state:
                state.has("Driver: Bean", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Battle Kukku XV"),
            lambda state:
                state.has("Driver: Tails", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Bean"),
            lambda state:
                state.has("Driver: Bark", world.player),
            "or"
        )
        
        add_rule(
            world.get_location("Challenge - Driver: Blaze"),
            lambda state:
                state.has("Driver: Silver", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Caterkiller"),
            lambda state:
                state.has("Driver: Motobug", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Chaos Zero"),
            lambda state:
                state.has("Driver: Tikal", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Charmy"),
            lambda state:
                state.has("Driver: Espio", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Heavy"),
            lambda state:
                state.has("Driver: Bomb", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Metal Knuckles"),
            lambda state:
                state.has("Driver: Metal Sonic", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Rouge"),
            lambda state:
                state.has("Driver: Knuckles", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Shadow"),
            lambda state:
                state.has("Driver: Sonic", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Silver"),
            lambda state:
                state.has("Driver: Blaze", world.player),
            "or"
        )

        add_rule(
            world.get_location("Challenge - Driver: Tikal"),
            lambda state:
                state.has("Driver: Chaos Zero", world.player),
            "or"
        )


def set_follower_challenge_location_rules(world: RingRacersWorld) -> None:
    set_rule(
        world.get_location("Challenge - Follower: Motobuddy"),
        lambda state:
            state.can_reach_region("Motobug Motorway", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Buzz Bomber"),
        lambda state:
            state.can_reach_region("Honeycomb Hollow", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Newtron"),
        lambda state:
            map_spb_attack(state, "Mega Green Hill", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Orbinaut"),
        lambda state:
            can_reach_sealed_star(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Jaws"),
        lambda state:
            state.has("Driver: Sonic", world.player)
            and state.can_reach_region("Labyrinth", world.player)
    )

    #
    # "Challenge - Follower: Bomb" is always possible, currently
    #

    #
    # "Challenge - Follower: Motobricks" is always possible...
    # ...but it's forced playtime, so make it always filler
    #
    motobricks_location = world.get_location("Challenge - Follower: Motobricks")
    motobricks_location.progress_type = LocationProgressType.EXCLUDED

    set_rule(
        world.get_location("Challenge - Follower: Uni-Uni"),
        lambda state:
            map_mystic_melody(state, "Star Light", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Chaos Emerald"),
        lambda state: # TODO: do we need to also check if we can reach the Sealed Stars themselves, too?
            can_reach_chaos_emeralds(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Anton"),
        lambda state:
            state.can_reach_region("Palmtree Panic", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mosqui"),
        lambda state:
            state.has("Driver: Amy", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Ga"),
        lambda state:
            map_mystic_melody(state, "Collision Chaos", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Tonbo"),
        lambda state:
            map_spb_attack(state, "Lavender Shrine", world.player)
    )

    #
    # "Challenge - Follower: Poh-Bee" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Follower: Bata-pyon"),
        lambda state:
            state.can_reach_region("Spring Yard", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Kabasira"),
        lambda state:
            state.has("Driver: Metal Sonic", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Hotaru"),
        lambda state:
            state.can_reach_region("Trap Tower", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: UFO"),
        lambda state:
            (state.has("Driver: Silver", world.player) and state.can_reach_region("CD Special Stage 8", world.player))
            or map_prison_break(state, "CD Special Stage 8", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Goddess"),
        lambda state:
            map_time_attack(state, "Angel Arrow Classic", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Sol"),
        lambda state:
            map_time_attack(state, "Hill Top", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Flasher"),
        lambda state:
            state.can_reach_region("Mystic Cave", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Jellygnite"),
        lambda state:
            (state.has("Encore Mode", world.player) and state.can_reach_region("Hydro City", world.player))
            or map_mystic_melody(state, "Sunbeam Paradise: Controls", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Aquis"),
        lambda state:
            map_mystic_melody(state, "Storm Rig", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Octus"),
        lambda state:
            map_mystic_melody(state, "Rusty Rig", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Asteron"),
        lambda state:
            state.can_reach_region("Hard-Boiled Stadium", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Egg Pod"),
        lambda state:
            state.has("Driver: Dr. Eggman", world.player)
            and state.can_reach_region("Metropolis", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Nebula"),
        lambda state:
            state.has("Follower: Tornado", world.player)
            and state.can_reach_region("SilverCloud Island", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Tornado"),
        lambda state:
            state.can_reach_region("Angel Island", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Meramora Jr."),
        lambda state:
            state.has("Driver: Caterkiller", world.player)
            and state.can_reach_region("Angel Island", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Buggernaut"),
        lambda state:
            state.can_reach_region("Pestilence", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bubbles"),
        lambda state:
            state.can_reach_region("Marble Garden", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Balloon"),
        lambda state:
            state.can_reach_region("Carnival Night", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Barrel"),
        lambda state:
            state.can_reach_region("Carnival Night", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mushmeanie"),
        lambda state:
            (state.has("Driver: Cluckoid", world.player) and state.can_reach_region("Tree Ring", world.player))
            or map_prison_break(state, "Fungal Dimension", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Technosqueek"),
        lambda state:
            state.can_reach_region("Mega Flying Battery", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Chainspike"),
        lambda state:
            state.can_reach_region("Death Egg", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Spikebonker"),
        lambda state:
            state.can_reach_region("Death Egg", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Hyudoro"),
        lambda state:
            state.can_reach_region("Mega Sandopolis", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Super Emerald"),
        lambda state:
            can_reach_all_emeralds(state, world.player)
    )

    spb_jr_location = world.get_location("Challenge - Follower: S.P.B. Jr.")
    set_rule(
        spb_jr_location,
        lambda state:
            enough_medals(state, 777, world.player)
    )
    # Requires over 50% of medals, exclude
    spb_jr_location.progress_type = LocationProgressType.EXCLUDED

    # "Challenge - Follower: Prison Egg" has been nerfed to 40 Prisons rounds.
    # Getting this naturally expects 10 cups to be played in both Grand Prix
    # and in Prison Break Mode.
    set_rule(
        world.get_location("Challenge - Follower: Prison Egg"),
        lambda state:
            state.has_group("Cups", world.player, 10)
            and state.has("Prison Break Mode", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Burboom"),
        lambda state:
            state.has("Driver: Espio", world.player)
            and state.can_reach_region("Isolated Island", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bushbubble"),
        lambda state:
            state.can_reach_region("World 1 Map", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Gotcha"),
        lambda state:
            state.can_reach_region("Bigtime Breakdown", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Motorspike"),
        lambda state:
            state.has("Driver: Charmy", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Piranhy"),
        lambda state:
            map_mystic_melody(state, "Sunbeam Paradise: Rings", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Ticktock"),
        lambda state:
            map_time_attack(state, "Joypolis", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Scouter"),
        lambda state:
            state.has("Driver: Motobug", world.player)
            and state.can_reach_region("Gems Museum", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Snowman"),
        lambda state:
            state.can_reach_region("Blue Mountain 2", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Firefly"),
        lambda state:
            state.has("Driver: Flicky", world.player)
            and state.can_reach_region("SEGA Saturn", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Whirl"),
        lambda state:
            state.can_reach_region("Gust Planet", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mecha Hiyoko"),
        lambda state:
            state.can_reach_region("Aqueduct Crystal", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Silver Sonic"),
        lambda state:
            state.can_reach_region("Chaos Chute", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Frogger"),
        lambda state:
            state.has_all(("Driver: Big", "Follower: Froggy"), world.player)
            and state.can_reach_region("Wood", world.player)
    )

    #
    # "Challenge - Follower: Bombaberry" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Follower: Spidal Tap"),
        lambda state:
            state.can_reach_region("Robotnik Winter", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bomblur"),
        lambda state:
            have_vicious_mode(state, world.player)
            and state.can_reach_region("Turquoise Hill", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mukaka"),
        lambda state:
            state.has("Driver: Vectorman", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Sandoom"),
        lambda state:
            state.can_reach_region("Roasted Ruins", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Gaikoko"),
        lambda state:
            map_mystic_melody(state, "Haunted Ship", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Chao"),
        lambda state:
            state.has("Follower: Chao Egg", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Chao Egg"),
        lambda state:
            state.can_reach_region("Barrier Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Froggy"),
        lambda state:
            state.can_reach_region("Emerald Coast", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Spinner"),
        lambda state:
            state.has("Driver: Sonic", world.player)
            and state.can_reach_region("Speed Highway", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Kart Kiki"),
        lambda state:
            state.has("Driver: Metal Sonic", world.player)
    )

    #
    # "Challenge - Follower: Bowling Pin" is always possible, currently.
    # The condition has been nerfed to 1 minute instead of 10 to
    # make it less annoying.
    #

    set_rule(
        world.get_location("Challenge - Follower: Hint Orb"),
        lambda state:
            state.has("Driver: Tikal", world.player)
            and can_reach_sealed_star(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Jet Booster"),
        lambda state:
            state.can_reach_region("Hot Shelter", world.player)
    )

    chaclon_location = world.get_location("Challenge - Follower: Chaclon")
    set_rule(
        chaclon_location,
        lambda state:
            have_master_mode(state, world.player)
            and state.can_reach_region("Pico Park", world.player)
    )

    #if (medalsanity):
    #    add_rule(
    #        chaclon_location,
    #        lambda state:
    #            enough_medals(state, 200, world.player),
    #        "or"
    #    )

    set_rule(
        world.get_location("Challenge - Follower: Hero Chao"),
        lambda state:
            state.has_all(("Driver: Sonic", "Follower: Chao"), world.player)
            and state.can_reach_region("Hero Chao Garden", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Dark Chao"),
        lambda state:
            state.has_all(("Driver: Shadow", "Follower: Chao"), world.player)
            and state.can_reach_region("Dark Chao Garden", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mono Beetle"),
        lambda state:
            state.can_reach_region("City Escape", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Gold Beetle"),
        lambda state:
            state.can_reach_region("City Escape", world.player)
    )

    #
    # "Challenge - Follower: Attack Boo" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Follower: Boo"),
        lambda state:
            state.has("Driver: Rouge", world.player)
            and state.can_reach_region("Darkvile Castle 1", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Chaos Drive"),
        lambda state:
            can_reach_sealed_star(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Emerald Radar"),
        lambda state:
            state.has("Driver: Knuckles", world.player)
            and state.can_reach_region("Meteor Herd", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mystic Melody"),
        lambda state:
            state.can_reach_region("Lost Colony", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Cheese"),
        lambda state:
            state.has("Driver: Cream", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Egg Flapper"),
        lambda state:
            map_prison_break(state, "Power Plant", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Klagen"),
        lambda state:
            state.can_reach_region("Water Palace", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Gold Klagen"),
        lambda state:
            map_time_attack(state, "Water Palace", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Hermit Crab"),
        lambda state:
            state.can_reach_region("Sunbeam Paradise: Brakes", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Splats"),
        lambda state:
            map_mystic_melody(state, "Press Garden", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Marble UAP"),
        lambda state:
            map_prison_break(state, "Mega Marble", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Claw Guy"),
        lambda state:
            state.can_reach_region("Advent Angel", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bubbler's Mother"),
        lambda state:
            map_spb_attack(state, "Chemical Facility", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Spinpole"),
        lambda state:
            state.can_reach_region("Vermilion Vessel", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Flysquid"),
        lambda state:
            state.can_reach_region("Hydro Plant", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Final Duck"),
        lambda state:
            state.has("Driver: Billy Hatcher", world.player)
            and state.can_reach_region("Kodachrome Void", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Tridrill"),
        lambda state:
            have_vicious_mode(state, world.player)
            and state.can_reach_region("Rumble Ridge", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Cappy"),
        lambda state:
            have_vicious_mode(state, world.player)
            and state.can_reach_region("Recycle B Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Jetarang"),
        lambda state:
            state.can_reach_region("Recycle A Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Balldron"),
        lambda state:
            state.has("Driver: Metal Knuckles", world.player)
            and state.can_reach_region("Crimson Core", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bomber"),
        lambda state:
            have_vicious_mode(state, world.player)
            and state.can_reach_region("Ice Paradise", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Gyro"),
        lambda state:
            state.can_reach_region("Gravtech Dimension 5", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: SRB1 Crawla"),
        lambda state:
            have_vicious_mode(state, world.player)
            and state.can_reach_region("SRB2 Frozen Night", world.player)
            and (
                state.has_group("Engine Class C", world.player)
                or state.has_group("Engine Class F", world.player)
                or state.has_group("Engine Class I", world.player)
            )
    )

    set_rule(
        world.get_location("Challenge - Follower: GuardRobo"),
        lambda state:
            map_mystic_melody(state, "Technology Tundra", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: HotRobo"),
        lambda state:
            state.can_reach_region("Mega Lava Reef", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Pyrex"),
        lambda state:
            state.can_reach_region("Mega Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Spybot 2000"),
        lambda state:
            state.can_reach_region("Thunder Piston", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: SRB2 Crawla"),
        lambda state:
            state.has("Driver: Bomb", world.player)
            and state.can_reach_region("SRB2 Meadow Match", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mean Bean"),
        lambda state:
            state.has_all(("Driver: Dr. Eggman", "Follower: Has Bean"), world.player)
            and state.can_reach_region("Egg Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: C.H.R.O.M.E."),
        lambda state:
            state.can_reach_region("Virtual Highway", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Tridentz"),
        lambda state:
            state.can_reach_region("Nova Shore", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Stegospike"),
        lambda state:
            state.has("Driver: Redz", world.player)
            and state.can_reach_region("Nova Shore", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Flicky Turncoat"),
        lambda state:
            state.has("Driver: Flicky", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Manegg"),
        lambda state:
            map_mystic_melody(state, "Nova Shore", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Blend Eye"),
        lambda state:
            state.can_reach_region("Adventure Example", world.player)
    )

    #
    # "Challenge - Follower: Flicky" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Follower: Red Flicky"),
        lambda state:
            state.can_reach_region("Scarlet Gardens", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Pink Flicky"),
        lambda state:
            state.can_reach_region("Diamond Dust", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Green Flicky"),
        lambda state:
            state.can_reach_region("Regal Ruin", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Clucky"),
        lambda state:
            state.has("Driver: Cluckoid", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Fish"),
        lambda state:
            state.can_reach_region("Mega Aqua Lake", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Puffin"),
        lambda state:
            state.can_reach_region("Sub-Zero Peak", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Dove"),
        lambda state:
            state.can_reach_region("Flash Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Canary"),
        lambda state:
            state.can_reach_region("Endless Mine 1", world.player)
            and state.has_any(("Driver: Billy Hatcher", "Driver: Motobug"), world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bat"),
        lambda state:
            state.can_reach_region("Darkvile Castle 2", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Has Bean"),
        lambda state:
            state.has("Driver: Arle", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Nomi"),
        lambda state:
            state.has("Driver: Arle", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Glyph"),
        lambda state:
            state.has("Driver: Ecco", world.player)
            and state.can_reach_region("Crystal Island", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Asterite"),
        lambda state:
            map_mystic_melody(state, "Azure Axiom", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Controller"),
        lambda state:
            have_master_mode(state, world.player)
            and can_reach_all_emeralds(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Orblet"),
        lambda state:
            have_all_guest_drivers(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Kobu"),
        lambda state:
            state.can_reach_region("Hanagumi Hall", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: The Cake From Hell"),
        lambda state:
            state.has("Driver: Gutbuster", world.player)
            and state.can_reach_region("Spring Cup", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Billiards Cactus"),
        lambda state:
            state.has("Driver: AiAi", world.player)
            and state.can_reach_region("Mirage Saloon", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Mag"),
        lambda state:
            map_mystic_melody(state, "Las Vegas", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Bacura"),
        lambda state:
            map_prison_break(state, "Media Studio", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Cacodemon"),
        lambda state:
            map_prison_break(state, "Dead Simple", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Shade Core"),
        lambda state:
            state.has("Driver: Carol", world.player)
            and state.can_reach_region("Aqua Tunnel", world.player)
    )

    set_rule(
        world.get_location("Challenge - Follower: Ancient Gear"),
        lambda state:
            state.can_reach_region("The Egg Carrier: Playground", world.player)
    )


def set_cup_challenge_location_rules(world: RingRacersWorld) -> None:
    #
    # "Challenge - Ring Cup" is always possible, currently
    #

    #
    # Page 1-1's challenges: beat the previous cup
    #
    set_rule(
        world.get_location("Challenge - Sneaker Cup"),
        lambda state:
            state.has("Ring Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Spring Cup"),
        lambda state:
            state.has("Sneaker Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Barrier Cup"),
        lambda state:
            state.has("Spring Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Invincible Cup"),
        lambda state:
            state.has("Barrier Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Emerald Cup"),
        lambda state:
            state.has("Invincible Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Extra Cup"),
        lambda state:
            state.has("Emerald Cup Access", world.player)
            and state.can_reach_region("Sunbeam Paradise: Brakes", world.player)
    )

    #
    # Page 1-2's challenges: beat Extra cup
    #
    set_rule(
        world.get_location("Challenge - S.P.B. Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Rocket Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Aqua Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Lightning Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Flame Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Super Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
            and state.can_reach_region("Sunbeam Paradise: Drifting", world.player)
    )

    #
    # Egg Cup challenge: beat all previous cups
    #
    set_rule(
        world.get_location("Challenge - Egg Cup"),
        lambda state:
            state.has_all((
                "Ring Cup Access",
                "Sneaker Cup Access",
                "Spring Cup Access",
                "Barrier Cup Access",
                "Invincible Cup Access",
                "Emerald Cup Access",
                "Extra Cup Access",
                "S.P.B. Cup Access",
                "Rocket Cup Access",
                "Aqua Cup Access",
                "Lightning Cup Access",
                "Flame Cup Access",
                "Super Cup Access"
            ), world.player)
    )

    #
    # Page 2's challenges: beat all previous cups OR get the Chaos Emerald on previous page's corresponding cup.
    #
    # It is always possible to get the Chaos Emerald, so use logic for Chaos Emerald.
    # Might need to revisit this if we have a "no Sealed Stars" logic mode.
    #
    set_rule(
        world.get_location("Challenge - Goggles Cup"),
        lambda state:
            state.has("Ring Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Timer Cup"),
        lambda state:
            state.has("Sneaker Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Grow Cup"),
        lambda state:
            state.has("Spring Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Chao Cup"),
        lambda state:
            state.has("Barrier Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Wing Cup"),
        lambda state:
            state.has("Invincible Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Mega Cup"),
        lambda state:
            state.has("Emerald Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Phantom Cup"),
        lambda state:
            state.has("Extra Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Flash Cup"),
        lambda state:
            state.has("S.P.B. Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Swap Cup"),
        lambda state:
            state.has("Rocket Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Shrink Cup"),
        lambda state:
            state.has("Aqua Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Bomb Cup"),
        lambda state:
            state.has("Lightning Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Power Cup"),
        lambda state:
            state.has("Flame Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Genesis Cup"),
        lambda state:
            state.has("Super Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Skate Cup"),
        lambda state:
            state.has("Egg Cup Access", world.player)
    )

    #
    # Page 3's challenges: Beat last cup on previous row w/ Chaos Emerald
    #
    # Again, may need revisited, see Page 2
    #
    set_rule(
        world.get_location("Challenge - Recycle A Cup"),
        lambda state:
            state.has("Phantom Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Recycle B Cup"),
        lambda state:
            state.has("Skate Cup Access", world.player)
    )


def set_extras_challenge_location_rules(world: RingRacersWorld) -> None:
    #
    # "Challenge - Prison Break Mode" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Special Mode"),
        lambda state:
            can_reach_chaos_emeralds(state, world.player)
    )

    set_rule(
        world.get_location("Challenge - Gear 3 + GP Vicious Mode"),
        lambda state:
            state.has("Egg Cup Access", world.player)
            or state.can_reach_region("The Egg Carrier: Playground", world.player)
    )

    #
    # "Challenge - Time Attack Mode" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - GP Master Mode"),
        lambda state:
            can_reach_all_emeralds(state, world.player)
    )

    encore_location = world.get_location("Challenge - Encore Mode")
    set_rule(
        encore_location,
        lambda state:
            have_all_cups(state, world.player)
    )
    # Requires over 50% of cups, exclude
    encore_location.progress_type = LocationProgressType.EXCLUDED

    spb_attack_location = world.get_location("Challenge - SPB Attack Mode")
    set_rule(
        spb_attack_location,
        lambda state:
            state.has_all(("Encore Mode", "Time Attack Mode"), world.player)
            and enough_medals(state, 500, world.player)
    )
    # Requires over 50% of medals, exclude
    spb_attack_location.progress_type = LocationProgressType.EXCLUDED

    #
    # "Challenge - Online Play" is always possible, currently
    #

    #
    # "Challenge - Alternate Titlescreen" is always possible, currently
    #

    #
    # "Challenge - Egg TV" is always possible, currently
    #

    if locations.location_name_allowed(world, "Challenge - Sound Test"):
        sound_test_location = world.get_location("Challenge - Sound Test")
        set_rule(
            sound_test_location,
            lambda state:
                have_group_percentage(state, "Alt. Music", world.player, 25)
        )

    #
    # "Challenge - Playing with Addons" is always possible, currently
    #

    #
    # "Challenge - The Egg Carrier: Playground" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Sunbeam Paradise: Brakes"),
        lambda state:
            state.has("Ring Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Sunbeam Paradise: Drifting"),
        lambda state:
            state.has("Spring Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Sunbeam Paradise: Items"),
        lambda state:
            state.has("Invincible Cup Access", world.player)
    )

    set_rule(
        world.get_location("Challenge - Sunbeam Paradise: Springs"),
        lambda state:
            state.has_any(("Rocket Cup Access", "Goggles Cup Access"), world.player)
    )

    test_run_location = world.get_location("Challenge - Lost & Found: Test Run")
    set_rule(
        test_run_location,
        lambda state:
            have_all_maps_but_test_run(state, world.player)
    )
    # Requires over 50% of cups+maps, exclude
    # (even if you can load an addon to get out of logic)
    test_run_location.progress_type = LocationProgressType.EXCLUDED

    set_rule(
        world.get_location("Challenge - Lost & Found: Hidden Palace"),
        lambda state:
            state.can_reach_region("Hidden Palace", world.player)
    )

    #
    # "Challenge - Lost & Found: Test Track" is always possible, currently
    #

    set_rule(
        world.get_location("Challenge - Lost & Found: Route 1980"),
        lambda state:
            state.can_reach_region("Route 1980", world.player)
    )

    #
    # "Challenge - Lost & Found: Duel Busters" is always possible, currently
    #


def set_alt_music_challenge_location_rules(world: RingRacersWorld) -> None:
    if locations.location_group_allowed(world, "CD Milestones"):
        milestone_locations = list(world.location_name_groups["CD Milestones"])

        total_bonus_rounds = 0
        for index, cup_def in jsondata.rr_cup_defs.items():
            for map_index in cup_def["map_list"]:
                map_def = jsondata.rr_map_defs[map_index]
                if map_def["type"] == "battle":
                    total_bonus_rounds += 1

        cd_counter = 1
        for _ in milestone_locations:
            location_name = "Challenge - Prison Egg CD #{}".format(cd_counter)
            location = world.get_location(location_name)

            required_bonus_rounds = min(cd_counter, total_bonus_rounds)
            set_rule(
                location,
                lambda state, rounds=required_bonus_rounds:
                    state.has("!Bonus Round Reachable", world.player, rounds)
            )

            if required_bonus_rounds > total_bonus_rounds:
                # exclude this location, since it explicitly requires grinding
                location.progress_type = LocationProgressType.EXCLUDED

            cd_counter += 1

    # Don't forget this one weirdo
    if locations.location_name_allowed(world, "Challenge - Alt. Music: Popcorn Workshop"):
        popcorn_workshop_location = world.get_location("Challenge - Alt. Music: Popcorn Workshop")
        set_rule(
            popcorn_workshop_location,
            lambda state:
                map_time_attack(state, "Popcorn Workshop", world.player)
        )
        # Requires platinum medal
        popcorn_workshop_location.progress_type = LocationProgressType.EXCLUDED


def set_challenge_location_rules(world: RingRacersWorld) -> None:
    if locations.location_group_allowed(world, "Challenges"):
        set_driver_challenge_location_rules(world)
        set_follower_challenge_location_rules(world)
        set_cup_challenge_location_rules(world)
        set_extras_challenge_location_rules(world)

    set_alt_music_challenge_location_rules(world)


def set_all_location_rules(world: RingRacersWorld) -> None:
    set_challenge_location_rules(world)


def set_completion_condition(world: RingRacersWorld) -> None:
    # TODO: Add more goal types!
    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "!Cup Trophy", world.player, world.options.goal_num_trophies.value
    )
