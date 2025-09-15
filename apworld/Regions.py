from BaseClasses import MultiWorld, Region, Location, ItemClassification
from .Locations import challenge_locations_table, RingRacersLocation
from .Items import RingRacersItem

cup_layout = {
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
        #"Hidden Palace",
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
        #"Sealed Star: Balconies",
    ],
    "Timer Cup": [
        "Savannah Citadel",
        "Umbrella Rushwinds",
        "Avant Garden",
        "Bigtime Breakdown",
        "Vantablack Violet",
        "City Skyline",
        "Vantablack Atrium",
        #"Sealed Star: Church",
    ],
    "Grow Cup": [
        "Chaos Chute",
        "Dimension Disaster",
        "Aurora Atoll",
        "Daytona Speedway",
        "Turquoise Hill",
        "Dead Simple",
        "Martian Matrix",
        #"Sealed Star: Courtyard",
    ],
    "Chao Cup": [
        "Weiss Waterway",
        "Ice Paradise",
        "Sunsplashed Getaway",
        "Fae Falls",
        "Azure Axiom",
        "Dark Chao Garden",
        "Hero Chao Garden",
        #"Sealed Star: Villa",
    ],
    "Wing Cup": [
        "Hanagumi Hall",
        "Aerial Highlands",
        "Crispy Canyon",
        "Technology Tundra",
        "Operators Overspace",
        "Whirl Waters",
        "Deluged Metroplex",
        #"Sealed Star: Venice",
    ],
    "Mega Cup": [
        "Mega Green Hill",
        "Mega Bridge",
        "Mega Lava Reef",
        "Mega Ice Cap",
        "Mega Scrap Brain",
        "Mega Emerald Beach",
        "Mega Labyrinth",
        #"Sealed Star: Spikes",
    ],
    "Phantom Cup": [
        "Wavecrash Dimension",
        "Nightfall Dimension",
        "Voiddance Dimension",
        "Cloudtop Dimension",
        "Gravtech Dimension",
        "Fungal Dimension",
        "Astral Dimension",
        #"Sealed Star: Fountain",
    ],

    "Flash Cup": [
        "Espresso Lane",
        "Melty Manor",
        "Leaf Storm",
        "Lake Margorite",
        "Endless Mine 2",
        "Chaos Seraph",
        "Toy Kingdom",
        #"Sealed Star: Gallery",
    ],
    "Swap Cup": [
        "Cyan Belltower",
        "Quartz Quadrant",
        "Aqua Tunnel",
        "Water Palace",
        "Final Fall",
        "Aquatic Cathedral 1",
        "Aquatic Cathedral 2",
        #"Sealed Star: Alley",
    ],
    "Shrink Cup": [
        "Haunted Ship",
        "Robotnik Winter",
        "Dragonspire Sewer 1",
        "Abyss Garden",
        "Blizzard Peaks",
        "Frosty Courtyard",
        "Abyss Gate",
        #"Sealed Star: Steeple",
    ],
    "Bomb Cup": [
        "Vermilion Vessel",
        "Dragonspire Sewer 2",
        "Chemical Facility",
        "Coastal Temple",
        "Monkey Mall",
        "Sonic's Schoolhouse",
        "Record Attack",
        #"Sealed Star: Rooftops",
    ],
    "Power Cup": [
        "Ramp Park",
        "Advent Angel",
        "Pestilence",
        "Crimson Core",
        "Las Vegas",
        "Peanut Palace",
        "Hydro Plant",
        #"Sealed Star: Roulette",
    ],
    "Genesis Cup": [
        "Mega Collision Chaos",
        "Mega Star Light",
        "Mega Sandopolis",
        "Mega Aqua Lake",
        "Mega Flying Battery",
        "Mega Metropolis",
        "Mega Marble",
        #"Sealed Star: Towers",
    ],
    "Skate Cup": [
        "Sky Babylon",
        "Kodachrome Void",
        "Lavender Shrine",
        "Thunder Piston",
        "Dead Line",
        "Thunder Lab",
        "Malign Eggshrine",
        #"Sealed Star: Atlantis",
    ],

    "Recycle Cup A": [
        "SRB2 Frozen Night",
        "Barren Badlands",
        "Shuffle Square",
        "Blue Mountain Classic",
        "Angel Arrow Classic",
        "SRB2 Meadow Match",
        "Armored Armadillo",
        #"Sealed Star: Balconies",
    ],
    "Recycle Cup B": [
        "Cadillac Canyon Classic",
        "Diamond Dust Classic",
        "Blizzard Peaks Classic",
        "Launch Base Classic",
        "Lavender Shrine Classic",
        "Clucky Farms",
        "Dried Battledune",
        #"Sealed Star: Church",
    ],
}

cup_region_access = {
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

tutorials_layout = [
    "Sunbeam Paradise: Controls",
    "Sunbeam Paradise: Rings",
    "Sunbeam Paradise: Brakes",
    "Sunbeam Paradise: Drifting",
    "Sunbeam Paradise: Springs",
    "Test Track"
]

lostandfound_layout = [
    "Test Run",
    "Hidden Palace",
    "Test Track",
]

lostandfound_region_access = {
    "Test Run": "Test Run Access",
    "Hidden Palace": "Hidden Palace Access",
    "Test Track": "Test Track Access",
}

def create_subregion(name: str, base_region: Region, multiworld: MultiWorld, player: int) -> Region:
    sub_region = Region(name, player, multiworld)
    multiworld.regions.append(sub_region)
    base_region.connect(sub_region)
    if (name == "Death Egg"): # TEMPORARY CRAP
        victory_location = RingRacersLocation(player, "Victory", None, sub_region)
        victory_location.place_locked_item(RingRacersItem("Victory", ItemClassification.progression, None, player))
        sub_region.locations.append(victory_location)
    return sub_region

def create_regions(multiworld: MultiWorld, player: int):
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    challenge_grid_region = Region("Challenge Grid", player, multiworld)

    # Some challenges are tied to certain levels.
    # Since these are very hard to do programmatically,
    # we just manually specify rules for these locations in Rules.py
    challenge_grid_region.add_locations(challenge_locations_table, RingRacersLocation)
    multiworld.regions.append(challenge_grid_region)

    menu_region.connect(challenge_grid_region)

    tutorial_region = Region("Tutorial", player, multiworld)
    multiworld.regions.append(tutorial_region)
    for map_name in tutorials_layout:
        create_subregion(map_name, tutorial_region, multiworld, player)
    menu_region.connect(tutorial_region)

    for cup_name, cup_maps in cup_layout.items():
        new_cup_region = Region(cup_name, player, multiworld)
        multiworld.regions.append(new_cup_region)
        for map_name in cup_maps:
            create_subregion(map_name, new_cup_region, multiworld, player)
        menu_region.add_exits(
            {cup_name: cup_region_access[cup_name]},
            {cup_name: lambda state: state.has(cup_region_access[cup_name], player)}
        )

    lostandfound_region = Region("Lost & Found", player, multiworld)
    multiworld.regions.append(lostandfound_region)
    menu_region.connect(lostandfound_region)

    for map_name in lostandfound_layout:
        create_subregion(map_name, lostandfound_region, multiworld, player)
        lostandfound_region.add_exits(
            {map_name: lostandfound_region_access[map_name]},
            {map_name: lambda state: state.has(lostandfound_region_access[map_name], player)}
        )

