from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import RingRacersWorld


RACE_MAP_LIST = [
    "Robotnik Coaster",
    "Northern District",
    "Panic City",
    "Sonic Speedway",
    "Green Hills",
    "Emerald Coast",
    "Storm Rig",
    "Lucid Pass",
    "Autumn Ring",
    "Withering Chateau",
    "Popcorn Workshop",
    "Sundae Drive",
    "Cadillac Cascade",
    "Rumble Ridge",
    "Opulence",
    "Angel Island",
    "Roasted Ruins",
    "Obsidian Oasis",
    "Mirage Saloon",
    "Regal Ruin",
    "Isolated Island",
    "Gigapolis",
    "Darkvile Castle 1",
    "Bronze Lake",
    "Collision Chaos",
    "Emerald Hill",
    "Azure City",
    "Gust Planet",
    "Mystic Cave",
    "Joypolis",
    "Hill Top",
    "Marble Garden",
    "Silvercloud Island",
    "Sub-Zero Peak",
    "Launch Base",
    "Azure Lake",
    "Balloon Park",
    "Chrome Gadget",
    "Desert Palace",
    "Endless Mine 1",
    "Hard-Boiled Stadium",
    "Hardhat Havoc",
    "Press Garden",
    "Pico Park",
    "City Escape",
    "Palmtree Panic",
    "Darkvile Castle 2",
    "Scarlet Gardens",
    "Motobug Motorway",
    "Star Light",
    "Metropolis",
    "Frozen Production",
    "Aqueduct Crystal",
    "Nova Shore",
    "Hydro City",
    "Trap Tower",
    "Diamond Dust",
    "Blue Mountain 1",
    "Blue Mountain 2",
    "Speed Highway",
    "Carnival Night",
    "Virtual Highway",
    "Dark Fortress",
    "Spring Yard",
    "Labyrinth",
    "Hot Shelter",
    "Sky Sanctuary",
    "Lost Colony",
    #"Milky Way",
    "Death Egg",
    "765 Stadium",
    "Skyscraper Leaps",
    "Green Triangle",
    "Zoned City",
    "Sunset Hill",
    "Savannah Citadel",
    "Umbrella Rushwinds",
    "Avant Garden",
    "Bigtime Breakdown",
    "Vantablack Violet",
    "Chaos Chute",
    "Dimension Disaster",
    "Aurora Atoll",
    "Daytona Speedway",
    "Turquoise Hill",
    "Weiss Waterway",
    "Ice Paradise",
    "Sunsplashed Getaway",
    "Fae Falls",
    "Azure Axiom",
    "Hanagumi Hall",
    "Aerial Highlands",
    "Crispy Canyon",
    "Technology Tundra",
    "Operators Overspace",
    "Mega Green Hill",
    "Mega Bridge",
    "Mega Lava Reef",
    "Mega Ice Cap",
    "Mega Scrap Brain",
    "Wavecrash Dimension",
    "Nightfall Dimension",
    "Voiddance Dimension",
    "Cloudtop Dimension",
    "Gravtech Dimension",
    "Espresso Lane",
    "Melty Manor",
    "Leaf Storm",
    "Lake Margorite",
    "Endless Mine 2",
    "Cyan Belltower",
    "Quartz Quadrant",
    "Aqua Tunnel",
    "Water Palace",
    "Final Fall",
    "Haunted Ship",
    "Robotnik Winter",
    "Dragonspire Sewer 1",
    "Abyss Garden",
    "Blizzard Peaks",
    "Vermilion Vessel",
    "Dragonspire Sewer 2",
    "Chemical Facility",
    "Coastal Temple",
    "Monkey Mall",
    "Ramp Park",
    "Advent Angel",
    "Pestilence",
    "Crimson Core",
    "Las Vegas",
    "Mega Collision Chaos",
    "Mega Star Light",
    "Mega Sandopolis",
    "Mega Aqua Lake",
    "Mega Flying Battery",
    "Sky Babylon",
    "Kodachrome Void",
    "Lavender Shrine",
    "Thunder Piston",
    "Dead Line",
    "SRB2 Frozen Night",
    "Barren Badlands",
    "Shuffle Square",
    "Blue Mountain Classic",
    "Angel Arrow Classic",
    "Cadillac Canyon Classic",
    "Diamond Dust Classic",
    "Blizzard Peaks Classic",
    "Launch Base Classic",
    "Lavender Shrine Classic",
    "Test Run",
    "Hidden Palace",
    "Test Track",
    "Route 1980",
]


BATTLE_MAP_LIST = [
    "Municipal Meadow",
    "CD Special Stage 1",
    "Tinkerer's Arena",
    "Tricircle Marina",
    "Mystery Gate",
    "Rusty Rig",
    "Marble Foyer",
    "Rock World",
    "World 1 Map",
    "CD Special Stage 8",
    "SEGA Saturn",
    "Electra Clacker",
    "Thunder Top",
    "Tree Ring",
    "Frigid Cove",
    "Gizmo Bastion",
    "Carbon Crucible",
    "Security Hall",
    "Gems Museum",
    "Media Studio",
    "Honeycomb Hollow",
    "Wood",
    "Brawl Fort",
    "Crystal Island",
    "Cyber Arena",
    "Neon Resort",
    "Meteor Herd",
    "Death Egg's Eye",
    "Tails Lab",
    "Power Plant",
    "City Skyline",
    "Vantablack Atrium",
    "Dead Simple",
    "Martian Matrix",
    "Dark Chao Garden",
    "Hero Chao Garden",
    "Whirl Waters",
    "Deluged Metroplex",
    "Mega Emerald Beach",
    "Mega Labyrinth",
    "Fungal Dimension",
    "Astral Dimension",
    "Chaos Seraph",
    "Toy Kingdom",
    "Aquatic Cathedral 1",
    "Aquatic Cathedral 2",
    "Frosty Courtyard",
    "Abyss Gate",
    "Sonic's Schoolhouse",
    "Record Attack",
    "Peanut Palace",
    "Hydro Plant",
    "Mega Metropolis",
    "Mega Marble",
    "Thunder Lab",
    "Malign Eggshrine",
    "SRB2 Meadow Match",
    "Armored Armadillo",
    "Clucky Farms",
    "Dried Battledune",
    "Duel Busters",
]


SPECIAL_MAP_LIST = [
    "Sealed Star: Balconies",
    "Sealed Star: Church",
    "Sealed Star: Courtyard",
    "Sealed Star: Villa",
    "Sealed Star: Venice",
    "Sealed Star: Spikes",
    "Sealed Star: Fountain",
    "Sealed Star: Gallery",
    "Sealed Star: Alley",
    "Sealed Star: Steeple",
    "Sealed Star: Rooftops",
    "Sealed Star: Roulette",
    "Sealed Star: Towers",
    "Sealed Star: Atlantis",
]


TUTORIAL_MAP_LIST = [
    "Sunbeam Paradise: Playground",
    "Sunbeam Paradise: Controls",
    "Sunbeam Paradise: Rings",
    "Sunbeam Paradise: Brakes",
    "Sunbeam Paradise: Drifting",
    "Sunbeam Paradise: Items",
    "Sunbeam Paradise: Springs",
]


MAP_LIST = [
    *RACE_MAP_LIST,
    *BATTLE_MAP_LIST,
    *SPECIAL_MAP_LIST,
    *TUTORIAL_MAP_LIST,
    "Adventure Example" # Doesn't really fit anywhere
]


CUP_TO_ACCESS_ITEM = {
    "Ring Cup": "Ring Cup Access",
    "Sneaker Cup": "Sneaker Cup Access",
    "Spring Cup": "Spring Cup Access",
    "Barrier Cup": "Barrier Cup Access",
    "Invincible Cup": "Invincible Cup Access",
    "Emerald Cup": "Emerald Cup Access",
    "Extra Cup": "Extra Cup Access",

    "S.P.B. Cup": "S.P.B. Cup Access",
    "Rocket Cup": "Rocket Cup Access",
    "Aqua Cup": "Aqua Cup Access",
    "Lightning Cup": "Lightning Cup Access",
    "Flame Cup": "Flame Cup Access",
    "Super Cup": "Super Cup Access",
    "Egg Cup": "Egg Cup Access",

    "Goggles Cup": "Goggles Cup Access",
    "Timer Cup": "Timer Cup Access",
    "Grow Cup": "Grow Cup Access",
    "Chao Cup": "Chao Cup Access",
    "Wing Cup": "Wing Cup Access",
    "Mega Cup": "Mega Cup Access",
    "Phantom Cup": "Phantom Cup Access",

    "Flash Cup": "Flash Cup Access",
    "Swap Cup": "Swap Cup Access",
    "Shrink Cup": "Shrink Cup Access",
    "Bomb Cup": "Bomb Cup Access",
    "Power Cup": "Power Cup Access",
    "Genesis Cup": "Genesis Cup Access",
    "Skate Cup": "Skate Cup Access",

    "Recycle Cup A": "Recycle Cup A Access",
    "Recycle Cup B": "Recycle Cup B Access",
}

DEFAULT_CUP_LAYOUT = {
    "Ring Cup": [
        "Robotnik Coaster",
        "Northern District",
        "Panic City",
        "Sonic Speedway",
        "Green Hills",
        "Municipal Meadow",
        "CD Special Stage 1",
        "Sealed Star: Balconies",
    ],
    "Sneaker Cup": [
        "Emerald Coast",
        "Storm Rig",
        "Lucid Pass",
        "Autumn Ring",
        "Withering Chateau",
        "Tinkerer's Arena",
        "Tricircle Marina",
        "Sealed Star: Church",
    ],
    "Spring Cup": [
        "Popcorn Workshop",
        "Sundae Drive",
        "Cadillac Cascade",
        "Rumble Ridge",
        "Opulence",
        "Mystery Gate",
        "Rusty Rig",
        "Sealed Star: Courtyard",
    ],
    "Barrier Cup": [
        "Angel Island",
        "Roasted Ruins",
        "Obsidian Oasis",
        "Mirage Saloon",
        "Regal Ruin",
        "Marble Foyer",
        "Rock World",
        "Sealed Star: Villa",
    ],
    "Invincible Cup": [
        "Isolated Island",
        "Gigapolis",
        "Darkvile Castle 1",
        "Bronze Lake",
        "Collision Chaos",
        "World 1 Map",
        "CD Special Stage 8",
        "Sealed Star: Venice",
    ],
    "Emerald Cup": [
        "Emerald Hill",
        "Azure City",
        "Gust Planet",
        "Mystic Cave",
        "Joypolis",
        "SEGA Saturn",
        "Electra Clacker",
        "Sealed Star: Spikes",
    ],
    "Extra Cup": [
        "Hill Top",
        "Marble Garden",
        "Silvercloud Island",
        "Sub-Zero Peak",
        "Launch Base",
        "Thunder Top",
        "Tree Ring",
        "Sealed Star: Fountain",
    ],

    "S.P.B. Cup": [
        "Azure Lake",
        "Balloon Park",
        "Chrome Gadget",
        "Desert Palace",
        "Endless Mine 1",
        "Frigid Cove",
        "Gizmo Bastion",
        "Sealed Star: Gallery",
    ],
    "Rocket Cup": [
        "Hard-Boiled Stadium",
        "Hardhat Havoc",
        "Press Garden",
        "Pico Park",
        "City Escape",
        "Carbon Crucible",
        "Security Hall",
        "Sealed Star: Alley",
    ],
    "Aqua Cup": [
        "Palmtree Panic",
        "Darkvile Castle 2",
        "Scarlet Gardens",
        "Motobug Motorway",
        "Star Light",
        "Gems Museum",
        "Media Studio",
        "Sealed Star: Steeple",
    ],
    "Lightning Cup": [
        "Metropolis",
        "Frozen Production",
        "Aqueduct Crystal",
        "Nova Shore",
        "Hydro City",
        "Honeycomb Hollow",
        "Wood",
        "Sealed Star: Rooftops",
    ],
    "Flame Cup": [
        "Trap Tower",
        "Diamond Dust",
        "Blue Mountain 1",
        "Blue Mountain 2",
        "Speed Highway",
        "Brawl Fort",
        "Crystal Island",
        "Sealed Star: Roulette",
    ],
    "Super Cup": [
        "Carnival Night",
        "Virtual Highway",
        "Dark Fortress",
        "Spring Yard",
        "Labyrinth",
        "Cyber Arena",
        "Neon Resort",
        "Sealed Star: Towers",
    ],
    "Egg Cup": [
        "Hot Shelter",
        "Sky Sanctuary",
        "Lost Colony",
        #"Milky Way",
        "Death Egg",
        "Meteor Herd",
        "Death Egg's Eye",
        "Sealed Star: Atlantis",
    ],

    "Goggles Cup": [
        "765 Stadium",
        "Skyscraper Leaps",
        "Green Triangle",
        "Zoned City",
        "Sunset Hill",
        "Tails Lab",
        "Power Plant",
        "Sealed Star: Balconies",
    ],
    "Timer Cup": [
        "Savannah Citadel",
        "Umbrella Rushwinds",
        "Avant Garden",
        "Bigtime Breakdown",
        "Vantablack Violet",
        "City Skyline",
        "Vantablack Atrium",
        "Sealed Star: Church",
    ],
    "Grow Cup": [
        "Chaos Chute",
        "Dimension Disaster",
        "Aurora Atoll",
        "Daytona Speedway",
        "Turquoise Hill",
        "Dead Simple",
        "Martian Matrix",
        "Sealed Star: Courtyard",
    ],
    "Chao Cup": [
        "Weiss Waterway",
        "Ice Paradise",
        "Sunsplashed Getaway",
        "Fae Falls",
        "Azure Axiom",
        "Dark Chao Garden",
        "Hero Chao Garden",
        "Sealed Star: Villa",
    ],
    "Wing Cup": [
        "Hanagumi Hall",
        "Aerial Highlands",
        "Crispy Canyon",
        "Technology Tundra",
        "Operators Overspace",
        "Whirl Waters",
        "Deluged Metroplex",
        "Sealed Star: Venice",
    ],
    "Mega Cup": [
        "Mega Green Hill",
        "Mega Bridge",
        "Mega Lava Reef",
        "Mega Ice Cap",
        "Mega Scrap Brain",
        "Mega Emerald Beach",
        "Mega Labyrinth",
        "Sealed Star: Spikes",
    ],
    "Phantom Cup": [
        "Wavecrash Dimension",
        "Nightfall Dimension",
        "Voiddance Dimension",
        "Cloudtop Dimension",
        "Gravtech Dimension",
        "Fungal Dimension",
        "Astral Dimension",
        "Sealed Star: Fountain",
    ],

    "Flash Cup": [
        "Espresso Lane",
        "Melty Manor",
        "Leaf Storm",
        "Lake Margorite",
        "Endless Mine 2",
        "Chaos Seraph",
        "Toy Kingdom",
        "Sealed Star: Gallery",
    ],
    "Swap Cup": [
        "Cyan Belltower",
        "Quartz Quadrant",
        "Aqua Tunnel",
        "Water Palace",
        "Final Fall",
        "Aquatic Cathedral 1",
        "Aquatic Cathedral 2",
        "Sealed Star: Alley",
    ],
    "Shrink Cup": [
        "Haunted Ship",
        "Robotnik Winter",
        "Dragonspire Sewer 1",
        "Abyss Garden",
        "Blizzard Peaks",
        "Frosty Courtyard",
        "Abyss Gate",
        "Sealed Star: Steeple",
    ],
    "Bomb Cup": [
        "Vermilion Vessel",
        "Dragonspire Sewer 2",
        "Chemical Facility",
        "Coastal Temple",
        "Monkey Mall",
        "Sonic's Schoolhouse",
        "Record Attack",
        "Sealed Star: Rooftops",
    ],
    "Power Cup": [
        "Ramp Park",
        "Advent Angel",
        "Pestilence",
        "Crimson Core",
        "Las Vegas",
        "Peanut Palace",
        "Hydro Plant",
        "Sealed Star: Roulette",
    ],
    "Genesis Cup": [
        "Mega Collision Chaos",
        "Mega Star Light",
        "Mega Sandopolis",
        "Mega Aqua Lake",
        "Mega Flying Battery",
        "Mega Metropolis",
        "Mega Marble",
        "Sealed Star: Towers",
    ],
    "Skate Cup": [
        "Sky Babylon",
        "Kodachrome Void",
        "Lavender Shrine",
        "Thunder Piston",
        "Dead Line",
        "Thunder Lab",
        "Malign Eggshrine",
        "Sealed Star: Atlantis",
    ],

    "Recycle Cup A": [
        "SRB2 Frozen Night",
        "Barren Badlands",
        "Shuffle Square",
        "Blue Mountain Classic",
        "Angel Arrow Classic",
        "SRB2 Meadow Match",
        "Armored Armadillo",
        "Sealed Star: Balconies",
    ],
    "Recycle Cup B": [
        "Cadillac Canyon Classic",
        "Diamond Dust Classic",
        "Blizzard Peaks Classic",
        "Launch Base Classic",
        "Lavender Shrine Classic",
        "Clucky Farms",
        "Dried Battledune",
        "Sealed Star: Church",
    ],
}

LOST_AND_FOUND_TO_ACCESS_ITEM = {
    "Test Run": "Test Run Access",
    "Hidden Palace": "Hidden Palace Access",
    "Test Track": "Test Track Access",
    "Route 1980": "Route 1980 Access",
    "Duel Busters": "Duel Busters Access",
}

def create_and_connect_regions(world: APQuestWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: APQuestWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    challenges = Region("Challenge Grid", world.player, world.multiworld)
    tutorial = Region("Tutorial", world.player, world.multiworld)
    lost_n_found = Region("Lost & Found", world.player, world.multiworld)

    regions = [menu, challenges, tutorial, lost_n_found]

    for cup_name in CUP_TO_ACCESS_ITEM:
        cup_region = Region(cup_name, world.player, world.multiworld)
        regions.append(cup_region)

    for map_name in MAP_LIST:
        map_region = Region(map_name, world.player, world.multiworld)
        regions.append(map_region)

    world.multiworld.regions += regions


def connect_regions(world: APQuestWorld) -> None:
    menu = world.get_region("Menu")

    challenges = world.get_region("Challenge Grid")
    menu.connect(challenges, "Menu to Challenge Grid")

    # Connect cups to menu, and then the cup's levels to the cup
    for cup_name, cup_maps in DEFAULT_CUP_LAYOUT.items():
        cup_region = world.get_region(cup_name)

        # We'll set cup access item here because it's easy enough.
        # More specific rules are handled in rules.py
        menu.connect(cup_region, "Menu to " + cup_name)

        for map_name in cup_maps:
            map_region = world.get_region(map_name)
            cup_region.connect(map_region, cup_name + " to " + map_name)

    # Lost & Found
    lost_n_found_region = world.get_region("Lost & Found")
    menu.connect(lost_n_found_region, "Menu to Lost & Found")

    for map_name in LOST_AND_FOUND_TO_ACCESS_ITEM.keys():
        map_region = world.get_region(map_name)
        lost_n_found_region.connect(map_region, "Lost & Found to " + map_name)

    # Tutorial
    tutorial_region = world.get_region("Tutorial")
    menu.connect(tutorial_region, "Menu to Tutorial")

    for map_name in TUTORIAL_MAP_LIST:
        map_region = world.get_region(map_name)
        tutorial_region.connect(map_region, "Tutorial to " + map_name)

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
