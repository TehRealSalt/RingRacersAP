import typing
from BaseClasses import Item, ItemClassification, MultiWorld

class RingRacersItem(Item):
    game: str = "Dr. Robotnik’s Ring Racers"

driver_items = {
    "Driver: AiAi": 44330000,
    "Driver: Aigis": 44330001,
    "Driver: Arle": 44330002,
    "Driver: Azusa Miura": 44330003,
    "Driver: Bark": 44330004,
    "Driver: Battle Kukku XV": 44330005,
    "Driver: Bean": 44330006,
    "Driver: Big": 44330007,
    "Driver: Billy Hatcher": 44330008,
    "Driver: Blaze": 44330009,
    "Driver: Bomb": 44330010,
    "Driver: Carol": 44330011,
    "Driver: Caterkiller": 44330012,
    "Driver: Chao": 44330013,
    "Driver: Chaos": 44330014,
    "Driver: Charmy": 44330015,
    "Driver: Chuchu": 44330016,
    "Driver: Cluckoid": 44330017,
    "Driver: Cream": 44330018,
    "Driver: Ecco": 44330019,
    "Driver: Eggrobo": 44330020,
    "Driver: Emerl": 44330021,
    "Driver: Espio": 44330022,
    "Driver: Flicky": 44330023,
    "Driver: Gum": 44330024,
    "Driver: Gutbuster": 44330025,
    "Driver: Headdy": 44330026,
    "Driver: Heavy": 44330027,
    "Driver: Heavy Magician": 44330028,
    "Driver: Honey": 44330029,
    "Driver: Jack Frost": 44330030,
    "Driver: Jet": 44330031,
    "Driver: Orenzo": 44330032,
    "Driver: Mail": 44330033,
    "Driver: Maria": 44330034,
    "Driver: Mecha Sonic": 44330035,
    "Driver: Metal Knuckles": 44330036,
    "Driver: NiGHTS": 44330037,
    "Driver: Orta": 44330038,
    "Driver: Pulseman": 44330039,
    "Driver: Rappy": 44330040,
    "Driver: Ray": 44330041,
    "Driver: Redz": 44330042,
    "Driver: Rouge": 44330043,
    "Driver: Sakura Shinguji": 44330044,
    "Driver: Shadow": 44330045,
    "Driver: Silver": 44330046,
    "Driver: Surge": 44330047,
    "Driver: Tails Doll": 44330048,
    "Driver: Tikal": 44330049,
    "Driver: Vectorman": 44330050,
    "Driver: Whisper": 44330051,
    "Driver: Wonder Boy": 44330052,
    "Driver: Zipp": 44330053,
    "Driver: Ring the Racer": 44330054,
}

follower_items = {
    "Follower: Motobuddy": 44330119,
    "Follower: Buzz Bomber": 44330200,
    "Follower: Newtron": 44330201,
    "Follower: Orbinaut": 44330202,
    "Follower: Jaws": 44330203,
    "Follower: Bomb": 44330204,
    "Follower: Motobricks": 44330205,
    "Follower: Uni-Uni": 44330206,
    "Follower: Chaos Emerald": 44330207,

    "Follower: Anton": 44330214,
    "Follower: Mosqui": 44330215,
    "Follower: Ga": 44330216,
    "Follower: Tonbo": 44330217,
    "Follower: Poh-Bee": 44330218,
    "Follower: Bata-pyon": 44330219,
    "Follower: Kabasira": 44330220,
    "Follower: Hotaru": 44330221,
    "Follower: UFO": 44330222,
    "Follower: Goddess": 44330223,

    "Follower: Sol": 44330229,
    "Follower: Flasher": 44330230,
    "Follower: Jellygnite": 44330231,
    "Follower: Aquis": 44330232,
    "Follower: Octus": 44330233,
    "Follower: Asteron": 44330234,
    "Follower: Egg Pod": 44330235,
    "Follower: Nebula": 44330236,
    "Follower: Tornado": 44330237,

    "Follower: Meramora Jr.": 44330244,
    "Follower: Buggernaut": 44330245,
    "Follower: Bubbles": 44330246,
    "Follower: Balloon": 44330247,
    "Follower: Barrel": 44330248,
    "Follower: Mushmeanie": 44330249,
    "Follower: Technosqueek": 44330250,
    "Follower: Chainspike": 44330251,
    "Follower: Spikebonker": 44330252,
    "Follower: Hyudoro": 44330250,
    "Follower: Super Emerald": 44330251,
    "Follower: S.P.B. Jr.": 44330252,

    "Follower: Burboom": 44330260,
    "Follower: Bushbubble": 44330261,
    "Follower: Gotcha": 44330262,
    "Follower: Motorspike": 44330263,
    "Follower: Piranhy": 44330264,
    "Follower: Ticktock": 44330265,

    "Follower: Scouter": 44330275,
    "Follower: Snowman": 44330276,
    "Follower: Firefly": 44330277,
    "Follower: Whirl": 44330278,

    "Follower: Mecha Hiyoko": 44330290,
    "Follower: Silver Sonic": 44330291,
    "Follower: Frogger": 44330292,
    "Follower: Bombaberry": 44330293,
    "Follower: Spidal Tap": 44330294,
    "Follower: Bomblur": 44330295,
    "Follower: Mukaka": 44330296,
    "Follower: Sandoom": 44330297,
    "Follower: Gaikoko": 44330298,

    "Follower: Chao": 44330305,
    "Follower: Chao Egg": 44330306,
    "Follower: Froggy": 44330307,
    "Follower: Spinner": 44330308,
    "Follower: Kart Kiki": 44330309,
    "Follower: Bowling Pin": 44330310,
    "Follower: Hint Orb": 44330311,
    "Follower: Jet Booster": 44330312,
    "Follower: Chaclon": 44330313,

    "Follower: Hero Chao": 44330320,
    "Follower: Dark Chao": 44330321,
    "Follower: Mono Beetle": 44330322,
    "Follower: Gold Beetle": 44330323,
    "Follower: Attack Boo": 44330324,
    "Follower: Boo": 44330325,
    "Follower: Chaos Drive": 44330326,
    "Follower: Emerald Radar": 44330327,
    "Follower: Mystic Melody": 44330328,

    "Follower: Cheese": 44330335,
    "Follower: Egg Flapper": 44330336,
    "Follower: Klagen": 44330337,
    "Follower: Gold Klagen": 44330338,
    "Follower: Hermit Crab": 44330339,

    "Follower: Splats": 44330350,
    "Follower: Marble UAP": 44330351,
    "Follower: Claw Guy": 44330352,
    "Follower: Bubbler's Mother": 44330353,
    "Follower: Spinpole": 44330354,
    "Follower: Flysquid": 44330355,
    "Follower: Final Duck": 44330356,

    "Follower: Tridrill": 44330365,
    "Follower: Cappy": 44330366,
    "Follower: Jetarang": 44330367,
    "Follower: Balldron": 44330368,
    "Follower: Bomber": 44330369,
    "Follower: Gyro": 44330370,

    "Follower: SRB1 Crawla": 44330380,
    "Follower: GuardRobo": 44330381,
    "Follower: HotRobo": 44330382,
    "Follower: Pyrex": 44330383,
    "Follower: Spybot 2000": 44330384,

    "Follower: SRB2 Crawla": 44330395,
    "Follower: Mean Bean": 44330396,
    "Follower: C.H.R.O.M.E.": 44330397,
    "Follower: Tridentz": 44330398,
    "Follower: Stegospike": 44330399,
    "Follower: Flicky Turncoat": 44330400,
    "Follower: Manegg": 44330401,
    "Follower: Blend Eye": 44330402,

    "Follower: Flicky": 44330410,
    "Follower: Red Flicky": 44330411,
    "Follower: Pink Flicky": 44330412,
    "Follower: Green Flicky": 44330413,
    "Follower: Clucky": 44330414,
    "Follower: Fish": 44330415,
    "Follower: Puffin": 44330416,
    "Follower: Dove": 44330417,
    "Follower: Canary": 44330418,
    "Follower: Bat": 44330419,

    "Follower: Has Bean": 44330425,
    "Follower: Nomi": 44330426,
    "Follower: Glyph": 44330427,
    "Follower: Asterite": 44330428,
    "Follower: Controller": 44330429,
    "Follower: Orblet": 44330430,
    "Follower: Kobu": 44330431,
    "Follower: The Cake From Hell": 44330432,
    "Follower: Billiards Cactus": 44330433,
    "Follower: Mag": 44330434,
    "Follower: Bacura": 44330435,
    "Follower: Cacodemon": 44330436,
    "Follower: Shade Core": 44330437,
}

spraycan_items = {
    "Spray Can: Red": 44330499,
    "Spray Can: Crimson": 44330500,
    "Spray Can: Maroon": 44330501,
    "Spray Can: Lemonade": 44330502,
    "Spray Can: Scarlet": 44330503,
    "Spray Can: Ketchup": 44330504,
    "Spray Can: Dawn": 44330505,
    "Spray Can: Sunslam": 44330506,
    "Spray Can: Creamsicle": 44330507,
    "Spray Can: Orange": 44330508,
    "Spray Can: Rosewood": 44330509,
    "Spray Can: Tangerine": 44330510,
    "Spray Can: Tan": 44330511,
    "Spray Can: Cream": 44330512,
    "Spray Can: Gold": 44330513,
    "Spray Can: Royal": 44330514,
    "Spray Can: Bronze": 44330515,
    "Spray Can: Copper": 44330516,
    "Spray Can: Mustard": 44330517,
    "Spray Can: Banana": 44330518,
    "Spray Can: Olive": 44330519,
    "Spray Can: Crocodile": 44330520,
    "Spray Can: Peridot": 44330521,
    "Spray Can: Vomit": 44330522,
    "Spray Can: Garden": 44330523,
    "Spray Can: Lime": 44330524,
    "Spray Can: Handheld": 44330525,
    "Spray Can: Tea": 44330526,
    "Spray Can: Pistachio": 44330527,
    "Spray Can: Moss": 44330528,
    "Spray Can: Camouflage": 44330529,
    "Spray Can: Mint": 44330530,
    "Spray Can: Green": 44330531,
    "Spray Can: Pinetree": 44330532,
    "Spray Can: Turtle": 44330533,
    "Spray Can: Swamp": 44330534,
    "Spray Can: Dream": 44330535,
    "Spray Can: Plague": 44330536,
    "Spray Can: Emerald": 44330537,
    "Spray Can: Algae": 44330538,
    "Spray Can: Aquamarine": 44330539,
    "Spray Can: Turquoise": 44330540,
    "Spray Can: Teal": 44330541,
    "Spray Can: Robin": 44330542,
    "Spray Can: Cyan": 44330543,
    "Spray Can: Cerulean": 44330544,
    "Spray Can: Navy": 44330545,
    "Spray Can: Platinum": 44330546,
    "Spray Can: Slate": 44330547,
    "Spray Can: Steel": 44330548,
    "Spray Can: Thunder": 44330549,
    "Spray Can: Nova": 44330550,
    "Spray Can: Rust": 44330551,
    "Spray Can: Wristwatch": 44330552,
    "Spray Can: Jet": 44330553,
    "Spray Can: Sapphire": 44330554,
    "Spray Can: Ultramarine": 44330555,
    "Spray Can: Periwinkle": 44330556,
    "Spray Can: Blue": 44330557,
    "Spray Can: Midnight": 44330558,
    "Spray Can: Blueberry": 44330559,
    "Spray Can: Thistle": 44330560,
    "Spray Can: Purple": 44330561,
    "Spray Can: Pastel": 44330562,
    "Spray Can: Moonset": 44330563,
    "Spray Can: Dusk": 44330564,
    "Spray Can: Violet": 44330565,
    "Spray Can: Fuchsia": 44330566,
    "Spray Can: Toxic": 44330567,
    "Spray Can: Mauve": 44330568,
    "Spray Can: Lavender": 44330569,
    "Spray Can: Byzantium": 44330570,
    "Spray Can: Pomegranate": 44330571,
    "Spray Can: Lilac": 44330572,
    "Spray Can: Blossom": 44330573,
    "Spray Can: Taffy": 44330574,
    "Spray Can: White": 44330575,
    "Spray Can: Silver": 44330576,
    "Spray Can: Grey": 44330577,
    "Spray Can: Nickel": 44330578,
    "Spray Can: Black": 44330579,
    "Spray Can: Skunk": 44330580,
    "Spray Can: Fairy": 44330581,
    "Spray Can: Popcorn": 44330582,
    "Spray Can: Artichoke": 44330583,
    "Spray Can: Pigeon": 44330584,
    "Spray Can: Sepia": 44330585,
    "Spray Can: Beige": 44330586,
    "Spray Can: Caramel": 44330587,
    "Spray Can: Peach": 44330588,
    "Spray Can: Brown": 44330589,
    "Spray Can: Leather": 44330590,
    "Spray Can: Pink": 44330591,
    "Spray Can: Rose": 44330592,
    "Spray Can: Cinnamon": 44330593,
    "Spray Can: Ruby": 44330594,
    "Spray Can: Raspberry": 44330595,
    "Spray Can: Yellow": 44330596,
    "Spray Can: Magenta": 44330597,
    "Spray Can: Jawz": 44330598,
}

cup_access_items = {
    "Ring Cup Access": 44330600,
    "Sneaker Cup Access": 44330601,
    "Spring Cup Access": 44330602,
    "Barrier Cup Access": 44330603,
    "Invincible Cup Access": 44330604,
    "Emerald Cup Access": 44330605,
    "Extra Cup Access": 44330606,

    "S.P.B. Cup Access": 44330607,
    "Rocket Cup Access": 44330608,
    "Aqua Cup Access": 44330609,
    "Lightning Cup Access": 44330610,
    "Flame Cup Access": 44330611,
    "Super Cup Access": 44330612,
    "Egg Cup Access": 44330613,

    "Goggles Cup Access": 44330614,
    "Timer Cup Access": 44330615,
    "Grow Cup Access": 44330616,
    "Chao Cup Access": 44330617,
    "Wing Cup Access": 44330618,
    "Mega Cup Access": 44330619,
    "Phantom Cup Access": 44330620,

    "Flash Cup Access": 44330621,
    "Swap Cup Access": 44330622,
    "Shrink Cup Access": 44330623,
    "Bomb Cup Access": 44330624,
    "Power Cup Access": 44330625,
    "Genesis Cup Access": 44330626,
    "Skate Cup Access": 44330627,

    "Recycle Cup A Access": 44330628,
    "Recycle Cup B Access": 44330629,
}

extras_items = {
    "Prison Break Mode": 44330699,
    "Special Mode": 44330700,
    "Gear 3 + GP Vicious Mode": 44330701,
    "Time Attack Mode": 44330702,
    "GP Master Mode": 44330703,
    "Encore Mode": 44330704,
    "SPB Attack Mode": 44330705,

    "Online Play": 44330707,

    "Alternate Titlescreen": 44330729,
    "Egg TV": 44330730,
    "Sound Test": 44330731,
    "Playing with Addons": 44330732,
}

lostandfound_access_items = {
    "Test Run Access": 44330759,
    "Hidden Palace Access": 44330760,
    "Test Track Access": 44330761,
}

altmusic_items = {
    "Alt. Music: Test Run": 44330799,
    "Alt. Music: Emerald Coast A": 44330800,
    "Alt. Music: Emerald Coast B": 44330801,
    "Alt. Music: Angel Island A": 44330802,
    "Alt. Music: Angel Island B": 44330803,
    "Alt. Music: Regal Ruin A": 44330804,
    "Alt. Music: Regal Ruin B": 44330805,
    "Alt. Music: Collision Chaos": 44330806,
    "Alt. Music: Emerald Hill": 44330807,
    "Alt. Music: Gust Planet A": 44330808,
    "Alt. Music: Gust Planet B": 44330809,
    "Alt. Music: Mystic Cave A": 44330810,
    "Alt. Music: Mystic Cave B": 44330811,
    "Alt. Music: Marble Garden A": 44330812,
    "Alt. Music: Marble Garden B": 44330813,
    "Alt. Music: Launch Base A": 44330814,
    "Alt. Music: Launch Base B": 44330815,
    "Alt. Music: City Escape": 44330816,
    "Alt. Music: Palmtree Panic A": 44330817,
    "Alt. Music: Metropolis": 44330818,
    "Alt. Music: Hydro City A": 44330819,
    "Alt. Music: Hydro City B": 44330820,
    "Alt. Music: Diamond Dust": 44330821,
    "Alt. Music: Carnival Night A": 44330822,
    "Alt. Music: Carnival Night B": 44330823,
    "Alt. Music: Dark Fortress": 44330824,
    "Alt. Music: Hot Shelter": 44330825,
    "Alt. Music: Mega Lava Reef": 44330826,
    "Alt. Music: Quartz Quadrant": 44330827,
    "Alt. Music: Aqua Tunnel": 44330828,
    "Alt. Music: Abyss Garden": 44330829,
    "Alt. Music: Monkey Mall": 44330830,
    "Alt. Music: Crimson Core": 44330831,
    "Alt. Music: Mega Collision Chaos": 44330832,
    "Alt. Music: Diamond Dust Classic": 44330833,
    "Alt. Music: Nova Shore": 44330834,
    "Alt. Music: Weiss Waterway": 44330835,
    "Alt. Music: Mirage Saloon A": 44330836,
    "Alt. Music: Mirage Saloon B": 44330837,
    "Alt. Music: Hill Top": 44330838,
    "Alt. Music: Palmtree Panic B": 44330839,
    "Alt. Music: Test Track": 44330840,
    "Alt. Music: Thunder Piston": 44330841,
    "Alt. Music: Azure City": 44330842,

    "Alt. Music: CD Special Stage 1": 44330899,
    "Alt. Music: CD Special Stage 8": 44330900,
    "Alt. Music: Wood": 44330901,
    "Alt. Music: Rusty Rig": 44330902,
    "Alt. Music: Dead Simple": 44330903,
}

filler_items = {
    "Nothing": 44331024,
}

unlocks_table = {
    **driver_items,
    **follower_items,
    **spraycan_items,
    **cup_access_items,
    **extras_items,
    **lostandfound_access_items,
    **altmusic_items,
}

item_table = {
    **unlocks_table,
    **filler_items,
}

item_groups: typing.Dict[str, str] = {
    "Drivers":      list(driver_items.keys()),
    "Followers":    list(follower_items.keys()),
    "Spray Cans":   list(spraycan_items.keys()),
    "Cups":         list(cup_access_items.keys()),
    "Levels":       list(lostandfound_access_items.keys()),
    "Alt. Music":   list(altmusic_items.keys()),
    "Extras":       list(extras_items.keys()),
}

def create_item(name: str, player: int, classification: ItemClassification = ItemClassification.filler) -> RingRacersItem:
    return RingRacersItem(name, classification, item_table[name], player)

def create_items(multiworld: MultiWorld, player: int) -> None:
    items = []

    for item in sorted(item_groups["Extras"]):
        multiworld.push_precollected(create_item(item, player, ItemClassification.useful))

    #multiworld.push_precollected(create_item("Ring Cup Access", player, ItemClassification.progression))

    preplaced_items = {item.name for item in multiworld.precollected_items[player]}

    def add_item(item_name: str, item_class: ItemClassification):
        if item_name in preplaced_items:
            items.append(create_item("Nothing", player, ItemClassification.filler))
            return

        i = create_item(item_name, player, item_class)
        items.append(i)

    # Sort for deterministic order
    for item in sorted(item_groups["Cups"]):
        add_item(item, ItemClassification.progression)

    for item in sorted(item_groups["Levels"]):
        add_item(item, ItemClassification.progression)

    for item in sorted(item_groups["Drivers"]):
        add_item(item, ItemClassification.useful)

    for item in sorted(item_groups["Followers"]):
        add_item(item, ItemClassification.filler)

    for item in sorted(item_groups["Spray Cans"]):
        add_item(item, ItemClassification.filler)

    for item in sorted(item_groups["Alt. Music"]):
        add_item(item, ItemClassification.filler)

    multiworld.itempool += items
