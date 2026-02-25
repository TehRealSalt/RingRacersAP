from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import RingRacersWorld


CHALLENGE_DRIVER_LOCATION_NAME_TO_ID = {
    #
    # DRIVER CHALLENGES (1 - 199)
    #
    "Challenge - Driver: AiAi": 1,
    "Challenge - Driver: Aigis": 2,
    "Challenge - Driver: Arle": 3,
    "Challenge - Driver: Azusa Miura": 4,
    "Challenge - Driver: Bark": 5,
    "Challenge - Driver: Battle Kukku XV": 6,
    "Challenge - Driver: Bean": 7,
    "Challenge - Driver: Big": 8,
    "Challenge - Driver: Billy Hatcher": 9,
    "Challenge - Driver: Blaze": 10,
    "Challenge - Driver: Bomb": 11,
    "Challenge - Driver: Carol": 12,
    "Challenge - Driver: Caterkiller": 13,
    "Challenge - Driver: Chao": 14,
    "Challenge - Driver: Chaos": 15,
    "Challenge - Driver: Charmy": 16,
    "Challenge - Driver: Chuchu": 17,
    "Challenge - Driver: Cluckoid": 18,
    "Challenge - Driver: Cream": 19,
    "Challenge - Driver: Ecco": 20,
    "Challenge - Driver: Eggrobo": 21,
    "Challenge - Driver: Emerl": 22,
    "Challenge - Driver: Espio": 23,
    "Challenge - Driver: Flicky": 24,
    "Challenge - Driver: Gum": 25,
    "Challenge - Driver: Gutbuster": 26,
    "Challenge - Driver: Headdy": 27,
    "Challenge - Driver: Heavy": 28,
    "Challenge - Driver: Heavy Magician": 29,
    "Challenge - Driver: Honey": 30,
    "Challenge - Driver: Jack Frost": 31,
    "Challenge - Driver: Jet": 32,
    #"Challenge - Driver: Orenzo": 33,
    "Challenge - Driver: Mail": 34,
    "Challenge - Driver: Maria": 35,
    "Challenge - Driver: Mecha Sonic": 36,
    "Challenge - Driver: Metal Knuckles": 37,
    "Challenge - Driver: NiGHTS": 38,
    "Challenge - Driver: Orta": 39,
    "Challenge - Driver: Pulseman": 40,
    "Challenge - Driver: Rappy": 41,
    "Challenge - Driver: Ray": 42,
    "Challenge - Driver: Redz": 43,
    "Challenge - Driver: Rouge": 44,
    "Challenge - Driver: Sakura Shinguji": 45,
    "Challenge - Driver: Shadow": 46,
    "Challenge - Driver: Silver": 47,
    "Challenge - Driver: Surge": 48,
    "Challenge - Driver: Tails Doll": 49,
    "Challenge - Driver: Tikal": 50,
    "Challenge - Driver: Vectorman": 51,
    "Challenge - Driver: Whisper": 52,
    "Challenge - Driver: Wonder Boy": 53,
    "Challenge - Driver: Zipp": 54,
    "Challenge - Driver: Ring the Racer": 55,
    "Challenge - Driver: Trouble Bruin": 56,
}


CHALLENGE_FOLLOWER_LOCATION_NAME_TO_ID = {
    #
    # FOLLOWER CHALLENGES (200 - 499)
    #
    "Challenge - Follower: Motobuddy": 200,
    "Challenge - Follower: Buzz Bomber": 201,
    "Challenge - Follower: Newtron": 202,
    "Challenge - Follower: Orbinaut": 203,
    "Challenge - Follower: Jaws": 204,
    "Challenge - Follower: Bomb": 205,
    "Challenge - Follower: Motobricks": 206,
    "Challenge - Follower: Uni-Uni": 207,
    "Challenge - Follower: Chaos Emerald": 208,

    "Challenge - Follower: Anton": 215,
    "Challenge - Follower: Mosqui": 216,
    "Challenge - Follower: Ga": 217,
    "Challenge - Follower: Tonbo": 218,
    "Challenge - Follower: Poh-Bee": 219,
    "Challenge - Follower: Bata-pyon": 220,
    "Challenge - Follower: Kabasira": 221,
    "Challenge - Follower: Hotaru": 222,
    "Challenge - Follower: UFO": 223,
    "Challenge - Follower: Goddess": 224,

    "Challenge - Follower: Sol": 230,
    "Challenge - Follower: Flasher": 231,
    "Challenge - Follower: Jellygnite": 232,
    "Challenge - Follower: Aquis": 233,
    "Challenge - Follower: Octus": 234,
    "Challenge - Follower: Asteron": 235,
    "Challenge - Follower: Egg Pod": 236,
    "Challenge - Follower: Nebula": 237,
    "Challenge - Follower: Tornado": 238,

    "Challenge - Follower: Meramora Jr.": 245,
    "Challenge - Follower: Buggernaut": 246,
    "Challenge - Follower: Bubbles": 247,
    "Challenge - Follower: Balloon": 248,
    "Challenge - Follower: Barrel": 249,
    "Challenge - Follower: Mushmeanie": 250,
    "Challenge - Follower: Technosqueek": 251,
    "Challenge - Follower: Chainspike": 252,
    "Challenge - Follower: Spikebonker": 253,
    "Challenge - Follower: Hyudoro": 254,
    "Challenge - Follower: Super Emerald": 255,
    "Challenge - Follower: S.P.B. Jr.": 256,
    "Challenge - Follower: Prison Egg": 257,

    "Challenge - Follower: Burboom": 261,
    "Challenge - Follower: Bushbubble": 262,
    "Challenge - Follower: Gotcha": 263,
    "Challenge - Follower: Motorspike": 264,
    "Challenge - Follower: Piranhy": 265,
    "Challenge - Follower: Ticktock": 266,

    "Challenge - Follower: Scouter": 276,
    "Challenge - Follower: Snowman": 277,
    "Challenge - Follower: Firefly": 278,
    "Challenge - Follower: Whirl": 279,

    "Challenge - Follower: Mecha Hiyoko": 291,
    "Challenge - Follower: Silver Sonic": 292,
    "Challenge - Follower: Frogger": 293,
    "Challenge - Follower: Bombaberry": 294,
    "Challenge - Follower: Spidal Tap": 295,
    "Challenge - Follower: Bomblur": 296,
    "Challenge - Follower: Mukaka": 297,
    "Challenge - Follower: Sandoom": 298,
    "Challenge - Follower: Gaikoko": 299,

    "Challenge - Follower: Chao": 306,
    "Challenge - Follower: Chao Egg": 307,
    "Challenge - Follower: Froggy": 308,
    "Challenge - Follower: Spinner": 309,
    "Challenge - Follower: Kart Kiki": 310,
    "Challenge - Follower: Bowling Pin": 311,
    "Challenge - Follower: Hint Orb": 312,
    "Challenge - Follower: Jet Booster": 313,
    "Challenge - Follower: Chaclon": 314,

    "Challenge - Follower: Hero Chao": 321,
    "Challenge - Follower: Dark Chao": 322,
    "Challenge - Follower: Mono Beetle": 323,
    "Challenge - Follower: Gold Beetle": 324,
    "Challenge - Follower: Attack Boo": 325,
    "Challenge - Follower: Boo": 326,
    "Challenge - Follower: Chaos Drive": 327,
    "Challenge - Follower: Emerald Radar": 328,
    "Challenge - Follower: Mystic Melody": 329,

    "Challenge - Follower: Cheese": 336,
    "Challenge - Follower: Egg Flapper": 337,
    "Challenge - Follower: Klagen": 338,
    "Challenge - Follower: Gold Klagen": 339,
    "Challenge - Follower: Hermit Crab": 340,

    "Challenge - Follower: Splats": 351,
    "Challenge - Follower: Marble UAP": 352,
    "Challenge - Follower: Claw Guy": 353,
    "Challenge - Follower: Bubbler's Mother": 354,
    "Challenge - Follower: Spinpole": 355,
    "Challenge - Follower: Flysquid": 356,
    "Challenge - Follower: Final Duck": 357,

    "Challenge - Follower: Tridrill": 366,
    "Challenge - Follower: Cappy": 367,
    "Challenge - Follower: Jetarang": 368,
    "Challenge - Follower: Balldron": 369,
    "Challenge - Follower: Bomber": 370,
    "Challenge - Follower: Gyro": 371,

    "Challenge - Follower: SRB1 Crawla": 381,
    "Challenge - Follower: GuardRobo": 382,
    "Challenge - Follower: HotRobo": 383,
    "Challenge - Follower: Pyrex": 384,
    "Challenge - Follower: Spybot 2000": 385,

    "Challenge - Follower: SRB2 Crawla": 396,
    "Challenge - Follower: Mean Bean": 397,
    "Challenge - Follower: C.H.R.O.M.E.": 398,
    "Challenge - Follower: Tridentz": 399,
    "Challenge - Follower: Stegospike": 400,
    "Challenge - Follower: Flicky Turncoat": 401,
    "Challenge - Follower: Manegg": 402,
    "Challenge - Follower: Blend Eye": 403,

    "Challenge - Follower: Flicky": 411,
    "Challenge - Follower: Red Flicky": 412,
    "Challenge - Follower: Pink Flicky": 413,
    "Challenge - Follower: Green Flicky": 414,
    "Challenge - Follower: Clucky": 415,
    "Challenge - Follower: Fish": 416,
    "Challenge - Follower: Puffin": 417,
    "Challenge - Follower: Dove": 418,
    "Challenge - Follower: Canary": 419,
    "Challenge - Follower: Bat": 420,

    "Challenge - Follower: Has Bean": 426,
    "Challenge - Follower: Nomi": 427,
    "Challenge - Follower: Glyph": 428,
    "Challenge - Follower: Asterite": 429,
    "Challenge - Follower: Controller": 430,
    "Challenge - Follower: Orblet": 431,
    "Challenge - Follower: Kobu": 432,
    "Challenge - Follower: The Cake From Hell": 433,
    "Challenge - Follower: Billiards Cactus": 434,
    "Challenge - Follower: Mag": 435,
    "Challenge - Follower: Bacura": 436,
    "Challenge - Follower: Cacodemon": 437,
    "Challenge - Follower: Shade Core": 438,
    "Challenge - Follower: Ancient Gear": 439,
}



#CHALLENGE_SPRAY_CAN_LOCATION_NAME_TO_ID = {
    #
    # SPRAY CAN CHALLENGES (500 - 599)
    #

    # TODO: Maybe we want to allow a KKD medal per level,
    # instead of exactly 100 Spray Cans?
#}


CHALLENGE_CUP_LOCATION_NAME_TO_ID = {
    #
    # CUP CHALLENGES (600 - 699)
    #
    "Challenge - Ring Cup": 601,
    "Challenge - Sneaker Cup": 602,
    "Challenge - Spring Cup": 603,
    "Challenge - Barrier Cup": 604,
    "Challenge - Invincible Cup": 605,
    "Challenge - Emerald Cup": 606,
    "Challenge - Extra Cup": 607,

    "Challenge - S.P.B. Cup": 608,
    "Challenge - Rocket Cup": 609,
    "Challenge - Aqua Cup": 610,
    "Challenge - Lightning Cup": 611,
    "Challenge - Flame Cup": 612,
    "Challenge - Super Cup": 613,
    "Challenge - Egg Cup": 614,

    "Challenge - Goggles Cup": 615,
    "Challenge - Timer Cup": 616,
    "Challenge - Grow Cup": 617,
    "Challenge - Chao Cup": 618,
    "Challenge - Wing Cup": 619,
    "Challenge - Mega Cup": 620,
    "Challenge - Phantom Cup": 621,

    "Challenge - Flash Cup": 622,
    "Challenge - Swap Cup": 623,
    "Challenge - Shrink Cup": 624,
    "Challenge - Bomb Cup": 625,
    "Challenge - Power Cup": 626,
    "Challenge - Genesis Cup": 627,
    "Challenge - Skate Cup": 628,

    "Challenge - Recycle Cup A": 698,
    "Challenge - Recycle Cup B": 699,
}


CHALLENGE_EXTRAS_LOCATION_NAME_TO_ID = {
    #
    # MISC. CHALLENGES (700 - 799)
    #
    "Challenge - Prison Break Mode": 700,
    "Challenge - Special Mode": 701,
    "Challenge - Gear 3 + GP Vicious Mode": 702,
    "Challenge - Time Attack Mode": 703,
    "Challenge - GP Master Mode": 704,
    "Challenge - Encore Mode": 705,
    "Challenge - SPB Attack Mode": 706,

    "Challenge - Online Play": 708,

    "Challenge - Alternate Title Screen": 730,
    "Challenge - Egg TV": 731,
    "Challenge - Sound Test": 732,
    "Challenge - Playing with Addons": 733,

    "Challenge - Ancient Gear Playground": 750,
    "Challenge - Check Your Brakes": 751,
    "Challenge - The Art of Drifting": 752,
    "Challenge - The Item Gallery": 753,
    "Challenge - Springs & Trick Panels": 754,

    "Challenge - Lost & Found: Test Run": 760,
    "Challenge - Lost & Found: Hidden Palace": 761,
    "Challenge - Lost & Found: Test Track": 762,
    "Challenge - Lost & Found: Route 1980": 763,
    "Challenge - Lost & Found: Duel Busters": 764,

    "Challenge - Alt Music: Popcorn Workshop": 852,
}

#CHALLENGE_MUSIC_LOCATION_NAME_TO_ID = {
    #
    # PRISON EGG CD CHALLENGES (800 - 999)
    #

    # Similar story as Spray Cans; probably want per-level
    # instead of the global system.
#}


CHALLENGE_LOCATION_NAME_TO_ID = {
    **CHALLENGE_DRIVER_LOCATION_NAME_TO_ID,
    **CHALLENGE_FOLLOWER_LOCATION_NAME_TO_ID,
    #**CHALLENGE_COLOR_LOCATION_NAME_TO_ID,
    **CHALLENGE_CUP_LOCATION_NAME_TO_ID,
    **CHALLENGE_EXTRAS_LOCATION_NAME_TO_ID,
    #**CHALLENGE_MUSIC_LOCATION_NAME_TO_ID,
}


LOCATION_NAME_TO_ID = {
    **CHALLENGE_LOCATION_NAME_TO_ID
}


class RingRacersLocation(Location):
    game = "Dr. Robotnik's Ring Racers"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return { location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names }


def create_all_locations(world: RingRacersWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: RingRacersWorld) -> None:
    challenges = world.get_region("Challenge Grid")

    all_challenge_locations = get_location_names_with_ids(list(CHALLENGE_LOCATION_NAME_TO_ID.keys()))
    challenges.add_locations(all_challenge_locations, RingRacersLocation)


def create_events(world: RingRacersWorld) -> None:
    # TEMP: We are probably not going to make this our final goal
    death_egg_region = world.get_region("Death Egg")
    death_egg_region.add_event(
        "Egg Cup Complete", "Victory",
        location_type=RingRacersLocation, item_type=items.RingRacersItem
    )
