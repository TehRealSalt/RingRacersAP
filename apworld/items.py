from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import RingRacersWorld

DRIVER_ITEM_NAME_TO_ID = {
    #
    # DRIVERS (1 - 199)
    #
    "Driver: AiAi": 1,
    "Driver: Aigis": 2,
    "Driver: Arle": 3,
    "Driver: Azusa Miura": 4,
    "Driver: Bark": 5,
    "Driver: Battle Kukku XV": 6,
    "Driver: Bean": 7,
    "Driver: Big": 8,
    "Driver: Billy Hatcher": 9,
    "Driver: Blaze": 10,
    "Driver: Bomb": 11,
    "Driver: Carol": 12,
    "Driver: Caterkiller": 13,
    "Driver: Chao": 14,
    "Driver: Chaos": 15,
    "Driver: Charmy": 16,
    "Driver: Chuchu": 17,
    "Driver: Cluckoid": 18,
    "Driver: Cream": 19,
    "Driver: Ecco": 20,
    "Driver: Eggrobo": 21,
    "Driver: Emerl": 22,
    "Driver: Espio": 23,
    "Driver: Flicky": 24,
    "Driver: Gum": 25,
    "Driver: Gutbuster": 26,
    "Driver: Headdy": 27,
    "Driver: Heavy": 28,
    "Driver: Heavy Magician": 29,
    "Driver: Honey": 30,
    "Driver: Jack Frost": 31,
    "Driver: Jet": 32,
    #"Driver: Orenzo": 33,
    "Driver: Mail": 34,
    "Driver: Maria": 35,
    "Driver: Mecha Sonic": 36,
    "Driver: Metal Knuckles": 37,
    "Driver: NiGHTS": 38,
    "Driver: Orta": 39,
    "Driver: Pulseman": 40,
    "Driver: Rappy": 41,
    "Driver: Ray": 42,
    "Driver: Redz": 43,
    "Driver: Rouge": 44,
    "Driver: Sakura Shinguji": 45,
    "Driver: Shadow": 46,
    "Driver: Silver": 47,
    "Driver: Surge": 48,
    "Driver: Tails Doll": 49,
    "Driver: Tikal": 50,
    "Driver: Vectorman": 51,
    "Driver: Whisper": 52,
    "Driver: Wonder Boy": 53,
    "Driver: Zipp": 54,
    "Driver: Ring the Racer": 55,
    "Driver: Trouble Bruin": 56,

    "Driver: Tails": 191,
    "Driver: Amy": 192,
    "Driver: Sonic": 193,
    "Driver: Motobug": 194,
    "Driver: Knuckles": 195,
    "Driver: Fang": 196,
    "Driver: Mighty": 197,
    "Driver: Dr. Eggman": 198,
    "Driver: Metal Sonic": 199,
}

FOLLOWER_ITEM_NAME_TO_ID = {
    #
    # FOLLOWERS (200 - 499)
    #
    "Follower: Motobuddy": 200,
    "Follower: Buzz Bomber": 201,
    "Follower: Newtron": 202,
    "Follower: Orbinaut": 203,
    "Follower: Jaws": 204,
    "Follower: Bomb": 205,
    "Follower: Motobricks": 206,
    "Follower: Uni-Uni": 207,
    "Follower: Chaos Emerald": 208,

    "Follower: Anton": 215,
    "Follower: Mosqui": 216,
    "Follower: Ga": 217,
    "Follower: Tonbo": 218,
    "Follower: Poh-Bee": 219,
    "Follower: Bata-pyon": 220,
    "Follower: Kabasira": 221,
    "Follower: Hotaru": 222,
    "Follower: UFO": 223,
    "Follower: Goddess": 224,

    "Follower: Sol": 230,
    "Follower: Flasher": 231,
    "Follower: Jellygnite": 232,
    "Follower: Aquis": 233,
    "Follower: Octus": 234,
    "Follower: Asteron": 235,
    "Follower: Egg Pod": 236,
    "Follower: Nebula": 237,
    "Follower: Tornado": 238,

    "Follower: Meramora Jr.": 245,
    "Follower: Buggernaut": 246,
    "Follower: Bubbles": 247,
    "Follower: Balloon": 248,
    "Follower: Barrel": 249,
    "Follower: Mushmeanie": 250,
    "Follower: Technosqueek": 251,
    "Follower: Chainspike": 252,
    "Follower: Spikebonker": 253,
    "Follower: Hyudoro": 254,
    "Follower: Super Emerald": 255,
    "Follower: S.P.B. Jr.": 256,
    "Follower: Prison Egg": 257,

    "Follower: Burboom": 261,
    "Follower: Bushbubble": 262,
    "Follower: Gotcha": 263,
    "Follower: Motorspike": 264,
    "Follower: Piranhy": 265,
    "Follower: Ticktock": 266,

    "Follower: Scouter": 276,
    "Follower: Snowman": 277,
    "Follower: Firefly": 278,
    "Follower: Whirl": 279,

    "Follower: Mecha Hiyoko": 291,
    "Follower: Silver Sonic": 292,
    "Follower: Frogger": 293,
    "Follower: Bombaberry": 294,
    "Follower: Spidal Tap": 295,
    "Follower: Bomblur": 296,
    "Follower: Mukaka": 297,
    "Follower: Sandoom": 298,
    "Follower: Gaikoko": 299,

    "Follower: Chao": 306,
    "Follower: Chao Egg": 307,
    "Follower: Froggy": 308,
    "Follower: Spinner": 309,
    "Follower: Kart Kiki": 310,
    "Follower: Bowling Pin": 311,
    "Follower: Hint Orb": 312,
    "Follower: Jet Booster": 313,
    "Follower: Chaclon": 314,

    "Follower: Hero Chao": 321,
    "Follower: Dark Chao": 322,
    "Follower: Mono Beetle": 323,
    "Follower: Gold Beetle": 324,
    "Follower: Attack Boo": 325,
    "Follower: Boo": 326,
    "Follower: Chaos Drive": 327,
    "Follower: Emerald Radar": 328,
    "Follower: Mystic Melody": 329,

    "Follower: Cheese": 336,
    "Follower: Egg Flapper": 337,
    "Follower: Klagen": 338,
    "Follower: Gold Klagen": 339,
    "Follower: Hermit Crab": 340,

    "Follower: Splats": 351,
    "Follower: Marble UAP": 352,
    "Follower: Claw Guy": 353,
    "Follower: Bubbler's Mother": 354,
    "Follower: Spinpole": 355,
    "Follower: Flysquid": 356,
    "Follower: Final Duck": 357,

    "Follower: Tridrill": 366,
    "Follower: Cappy": 367,
    "Follower: Jetarang": 368,
    "Follower: Balldron": 369,
    "Follower: Bomber": 370,
    "Follower: Gyro": 371,

    "Follower: SRB1 Crawla": 381,
    "Follower: GuardRobo": 382,
    "Follower: HotRobo": 383,
    "Follower: Pyrex": 384,
    "Follower: Spybot 2000": 385,

    "Follower: SRB2 Crawla": 396,
    "Follower: Mean Bean": 397,
    "Follower: C.H.R.O.M.E.": 398,
    "Follower: Tridentz": 399,
    "Follower: Stegospike": 400,
    "Follower: Flicky Turncoat": 401,
    "Follower: Manegg": 402,
    "Follower: Blend Eye": 403,

    "Follower: Flicky": 411,
    "Follower: Red Flicky": 412,
    "Follower: Pink Flicky": 413,
    "Follower: Green Flicky": 414,
    "Follower: Clucky": 415,
    "Follower: Fish": 416,
    "Follower: Puffin": 417,
    "Follower: Dove": 418,
    "Follower: Canary": 419,
    "Follower: Bat": 420,

    "Follower: Has Bean": 426,
    "Follower: Nomi": 427,
    "Follower: Glyph": 428,
    "Follower: Asterite": 429,
    "Follower: Controller": 430,
    "Follower: Orblet": 431,
    "Follower: Kobu": 432,
    "Follower: The Cake From Hell": 433,
    "Follower: Billiards Cactus": 434,
    "Follower: Mag": 435,
    "Follower: Bacura": 436,
    "Follower: Cacodemon": 437,
    "Follower: Shade Core": 438,
    "Follower: Ancient Gear": 439,
}

COLOR_ITEM_NAME_TO_ID = {
    "Spray Can: Red": 500,
    "Spray Can: Crimson": 501,
    "Spray Can: Maroon": 502,
    "Spray Can: Lemonade": 503,
    "Spray Can: Scarlet": 504,
    "Spray Can: Ketchup": 505,
    "Spray Can: Dawn": 506,
    "Spray Can: Sunslam": 507,
    "Spray Can: Creamsicle": 508,
    "Spray Can: Orange": 509,
    "Spray Can: Rosewood": 510,
    "Spray Can: Tangerine": 511,
    "Spray Can: Tan": 512,
    "Spray Can: Cream": 513,
    "Spray Can: Gold": 514,
    "Spray Can: Royal": 515,
    "Spray Can: Bronze": 516,
    "Spray Can: Copper": 517,
    "Spray Can: Mustard": 518,
    "Spray Can: Banana": 519,
    "Spray Can: Olive": 520,
    "Spray Can: Crocodile": 521,
    "Spray Can: Peridot": 522,
    "Spray Can: Vomit": 523,
    "Spray Can: Garden": 524,
    "Spray Can: Lime": 525,
    "Spray Can: Handheld": 526,
    "Spray Can: Tea": 527,
    "Spray Can: Pistachio": 528,
    "Spray Can: Moss": 529,
    "Spray Can: Camouflage": 530,
    "Spray Can: Mint": 531,
    "Spray Can: Green": 532,
    "Spray Can: Pinetree": 533,
    "Spray Can: Turtle": 534,
    "Spray Can: Swamp": 535,
    "Spray Can: Dream": 536,
    "Spray Can: Plague": 537,
    "Spray Can: Emerald": 538,
    "Spray Can: Algae": 539,
    "Spray Can: Aquamarine": 540,
    "Spray Can: Turquoise": 541,
    "Spray Can: Teal": 542,
    "Spray Can: Robin": 543,
    "Spray Can: Cyan": 544,
    "Spray Can: Cerulean": 545,
    "Spray Can: Navy": 546,
    "Spray Can: Platinum": 547,
    "Spray Can: Slate": 548,
    "Spray Can: Steel": 549,
    "Spray Can: Thunder": 550,
    "Spray Can: Nova": 551,
    "Spray Can: Rust": 552,
    "Spray Can: Wristwatch": 553,
    "Spray Can: Jet": 554,
    "Spray Can: Sapphire": 555,
    "Spray Can: Ultramarine": 556,
    "Spray Can: Periwinkle": 557,
    "Spray Can: Blue": 558,
    "Spray Can: Midnight": 559,
    "Spray Can: Blueberry": 560,
    "Spray Can: Thistle": 561,
    "Spray Can: Purple": 562,
    "Spray Can: Pastel": 563,
    "Spray Can: Moonset": 564,
    "Spray Can: Dusk": 565,
    "Spray Can: Violet": 566,
    "Spray Can: Fuchsia": 567,
    "Spray Can: Toxic": 568,
    "Spray Can: Mauve": 569,
    "Spray Can: Lavender": 570,
    "Spray Can: Byzantium": 571,
    "Spray Can: Pomegranate": 572,
    "Spray Can: Lilac": 573,
    "Spray Can: Blossom": 574,
    "Spray Can: Taffy": 575,
    "Spray Can: White": 576,
    "Spray Can: Silver": 577,
    "Spray Can: Grey": 578,
    "Spray Can: Nickel": 579,
    "Spray Can: Black": 580,
    "Spray Can: Skunk": 581,
    "Spray Can: Fairy": 582,
    "Spray Can: Popcorn": 583,
    "Spray Can: Artichoke": 584,
    "Spray Can: Pigeon": 585,
    "Spray Can: Sepia": 586,
    "Spray Can: Beige": 587,
    "Spray Can: Caramel": 588,
    "Spray Can: Peach": 589,
    "Spray Can: Brown": 590,
    "Spray Can: Leather": 591,
    "Spray Can: Pink": 592,
    "Spray Can: Rose": 593,
    "Spray Can: Cinnamon": 594,
    "Spray Can: Ruby": 595,
    "Spray Can: Raspberry": 596,
    "Spray Can: Yellow": 597,
    "Spray Can: Magenta": 598,
    "Spray Can: Jawz": 599,
}

CUP_ITEM_NAME_TO_ID = {
    #
    # CUP ACCESS (600 - 699)
    #
    "Ring Cup Access": 601,
    "Sneaker Cup Access": 602,
    "Spring Cup Access": 603,
    "Barrier Cup Access": 604,
    "Invincible Cup Access": 605,
    "Emerald Cup Access": 606,
    "Extra Cup Access": 607,

    "S.P.B. Cup Access": 608,
    "Rocket Cup Access": 609,
    "Aqua Cup Access": 610,
    "Lightning Cup Access": 611,
    "Flame Cup Access": 612,
    "Super Cup Access": 613,
    "Egg Cup Access": 614,

    "Goggles Cup Access": 615,
    "Timer Cup Access": 616,
    "Grow Cup Access": 617,
    "Chao Cup Access": 618,
    "Wing Cup Access": 619,
    "Mega Cup Access": 620,
    "Phantom Cup Access": 621,

    "Flash Cup Access": 622,
    "Swap Cup Access": 623,
    "Shrink Cup Access": 624,
    "Bomb Cup Access": 625,
    "Power Cup Access": 626,
    "Genesis Cup Access": 627,
    "Skate Cup Access": 628,

    "Recycle Cup A Access": 698,
    "Recycle Cup B Access": 699,
}

EXTRAS_ITEM_NAME_TO_ID = {
    "Prison Break Mode": 700,
    "Special Mode": 701,
    "Gear 3 + GP Vicious Mode": 702,
    "Time Attack Mode": 703,
    "GP Master Mode": 704,
    "Encore Mode": 705,
    "SPB Attack Mode": 706,

    "Online Play": 708,

    "Alternate Title Screen": 730,
    "Egg TV": 731,
    "Sound Test": 732,
    "Play with Addons": 733,
}

MAP_ITEM_NAME_TO_ID = {
    "Sunbeam Paradise: Playground Access": 750,
    "Sunbeam Paradise: Brakes Access": 751,
    "Sunbeam Paradise: Drifting Access": 752,
    "Sunbeam Paradise: Items Access": 753,
    "Sunbeam Paradise: Springs Access": 754,

    "Test Run Access": 760,
    "Hidden Palace Access": 761,
    "Test Track Access": 762,
    "Route 1980 Access": 763,
    "Duel Busters Access": 764,
}

ALT_MUSIC_ITEM_NAME_TO_ID = {
    #
    # ALT MUSIC (800 - 999)
    #
    "Alt Music: Test Run": 800,
    "Alt Music: Emerald Coast (A)": 801,
    "Alt Music: Emerald Coast (B)": 802,
    "Alt Music: Angel Island (A)": 803,
    "Alt Music: Angel Island (B)": 804,
    "Alt Music: Regal Ruin (A)": 805,
    "Alt Music: Regal Ruin (B)": 806,
    "Alt Music: Collision Chaos": 807,
    "Alt Music: Emerald Hill": 808,
    "Alt Music: Gust Planet (A)": 809,
    "Alt Music: Gust Planet (B)": 810,
    "Alt Music: Mystic Cave (A)": 811,
    "Alt Music: Mystic Cave (B)": 812,
    "Alt Music: Marble Garden (A)": 813,
    "Alt Music: Marble Garden (B)": 814,
    "Alt Music: Launch Base (A)": 815,
    "Alt Music: Launch Base (B)": 816,
    "Alt Music: City Escape": 817,
    "Alt Music: Palmtree Panic (A)": 818,
    "Alt Music: Metropolis": 819,
    "Alt Music: Hydro City (A)": 820,
    "Alt Music: Hydro City (B)": 821,
    "Alt Music: Diamond Dust": 822,
    "Alt Music: Carnival Night (A)": 823,
    "Alt Music: Carnival Night (B)": 824,
    "Alt Music: Dark Fortress": 825,
    "Alt Music: Hot Shelter": 826,
    "Alt Music: Mega Lava Reef": 827,
    "Alt Music: Quartz Quadrant": 828,
    "Alt Music: Aqua Tunnel": 829,
    "Alt Music: Abyss Garden": 830,
    "Alt Music: Monkey Mall": 831,
    "Alt Music: Crimson Core": 832,
    "Alt Music: Mega Collision Chaos": 833,
    "Alt Music: Diamond Dust Classic": 834,
    "Alt Music: Nova Shore": 835,
    "Alt Music: Weiss Waterway": 836,
    "Alt Music: Mirage Saloon (A)": 837,
    "Alt Music: Mirage Saloon (B)": 838,
    "Alt Music: Hill Top": 839,
    "Alt Music: Palmtree Panic (B)": 840,
    "Alt Music: Test Track": 841,
    "Alt Music: Thunder Piston (A)": 842,
    "Alt Music: Azure City": 843,
    "Alt Music: Fae Falls": 844,
    "Alt Music: Speed Highway": 845,
    "Alt Music: Daytona Speedway": 846,
    "Alt Music: Storm Rig": 847,
    "Alt Music: Cadillac Cascade": 848,
    "Alt Music: Frozen Production": 849,
    "Alt Music: Cyan Belltower": 850,
    "Alt Music: Chaos Chute": 851,
    "Alt Music: Popcorn Workshop": 852,
    "Alt Music: Thunder Piston (B)": 853,

    "Alt Music: CD Special Stage 1": 900,
    "Alt Music: CD Special Stage 8": 901,
    "Alt Music: Wood": 902,
    "Alt Music: Rusty Rig": 903,
    "Alt Music: Dead Simple": 904,
    "Alt Music: Marble Foyer": 905,
    "Alt Music: Cyber Arena": 906,
    "Alt Music: Duel Buster": 907,
}


AP_ITEM_NAME_TO_ID = {
    #
    # ARCHIPELAGO ITEMS (10000+)
    #
    "Temporary Placeholder": 10000, # TODO: Remove
}


ITEM_NAME_TO_ID = {
    **DRIVER_ITEM_NAME_TO_ID,
    **FOLLOWER_ITEM_NAME_TO_ID,
    **COLOR_ITEM_NAME_TO_ID,
    **CUP_ITEM_NAME_TO_ID,
    **EXTRAS_ITEM_NAME_TO_ID,
    **MAP_ITEM_NAME_TO_ID,
    **ALT_MUSIC_ITEM_NAME_TO_ID,
    **AP_ITEM_NAME_TO_ID,
}


ITEM_NAME_GROUPS: typing.Dict[str, str] = {
    "Drivers": list(DRIVER_ITEM_NAME_TO_ID.keys()),
    "Followers": list(FOLLOWER_ITEM_NAME_TO_ID.keys()),
    "Spray Cans": list(COLOR_ITEM_NAME_TO_ID.keys()),
    "Cups": list(CUP_ITEM_NAME_TO_ID.keys()),
    "Maps": list(MAP_ITEM_NAME_TO_ID.keys()),
    "Alt Music": list(ALT_MUSIC_ITEM_NAME_TO_ID.keys()),
    "Extras": list(EXTRAS_ITEM_NAME_TO_ID.keys()),
}

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
    return "Temporary Placeholder"


def create_rr_item(world: RingRacersWorld, name: str) -> RingRacersItem:
    classification = ItemClassification.filler

    if name == "Follower: Mystic Melody":
        classification = ItemClassification.progression
    elif name in CHALLENGE_FOLLOWERS:
        # Only mark followers that are required for challenges as progression
        classification = ItemClassification.progression_deprioritized_skip_balancing
    elif name in ITEM_NAME_GROUPS["Drivers"]:
        # There's probably 1 or 2 drivers that aren't required for challenges,
        # but the vast majority of them are, so just mark them all as progression
        # and be done with it LOL
        classification = ItemClassification.progression_skip_balancing | ItemClassification.useful
    elif (name in ITEM_NAME_GROUPS["Cups"]
        or name in ITEM_NAME_GROUPS["Maps"]
        or name in ITEM_NAME_GROUPS["Extras"]):
        classification = ItemClassification.progression

    return RingRacersItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: RingRacersWorld) -> None:
    driver_pool: list[Item] = []

    for driver_name in DRIVER_ITEM_NAME_TO_ID.keys():
        driver_pool.append(world.create_item(driver_name))

    cup_pool: list[Item] = []

    for cup_name in CUP_ITEM_NAME_TO_ID.keys():
        cup_pool.append(world.create_item(cup_name))

    item_pool: list[Item] = []
    item_pool += driver_pool
    item_pool += cup_pool

    for follower_name in FOLLOWER_ITEM_NAME_TO_ID.keys():
        item_pool.append(world.create_item(follower_name))

    for map_name in MAP_ITEM_NAME_TO_ID.keys():
        item_pool.append(world.create_item(map_name))

    for extra_name in EXTRAS_ITEM_NAME_TO_ID.keys():
        item_pool.append(world.create_item(extra_name))

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
