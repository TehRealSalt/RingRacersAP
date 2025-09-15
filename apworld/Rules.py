from BaseClasses import MultiWorld, Location, CollectionState
from ..generic.Rules import add_rule, set_rule

from . import Items, Locations

def hundred_wins(state: CollectionState, driver_item: str, player: int) -> bool:
    # These are long, make them out of logic. Maybe tie to an option later.
    return False #return state.has(driver_item, player)

def map_mystic_melody(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("Follower: Mystic Melody", player)
        and state.can_reach(map_name, 'Region', player)
    )

def map_time_attack(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("Time Attack Mode", player)
        and state.can_reach(map_name, 'Region', player)
    )

def map_prison_break(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("Prison Break Mode", player)
        and state.can_reach(map_name, 'Region', player)
    )

def map_spb_attack(state: CollectionState, map_name: str, player: int) -> bool:
    return (
        state.has("SPB Attack Mode", player)
        and state.can_reach(map_name, 'Region', player)
    )

sealed_star_names = [
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

def can_reach_sealed_star(state: CollectionState, player: int) -> bool:
    for map_name in sealed_star_names:
        if (state.can_reach(map_name, 'Region', player)):
            return True
    return False

def have_all_cups(state: CollectionState, player: int) -> bool:
    for cup_name in Items.cup_access_items:
        if not (state.has(cup_name, player)):
            return False
    return True

def have_all_levels_but_test_run(state: CollectionState, player: int) -> bool:
    for cup_name in Items.cup_access_items:
        if not (state.has(cup_name, player)):
            return False

    for level_name in Items.lostandfound_access_items:
        if (level_name == "Test Run Access"):
            continue
        if not (state.has(level_name, player)):
            return False

    return True

def create_challenges_drivers_rules(multiworld: MultiWorld, player: int):
    set_rule(
        multiworld.get_location("Challenge - Driver: AiAi", player),
        lambda state:
            state.can_reach("Monkey Mall", 'Region', player)
            and state.has("Gear 3 + GP Vicious Mode", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Aigis", player),
        lambda state:
            state.can_reach("Operators Overspace", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Azusa Miura", player),
        lambda state:
            (state.has("Driver: Honey", player) and state.can_reach("765 Stadium", 'Region', player))
            or map_mystic_melody(state, "765 Stadium", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Arle", player),
        lambda state:
            map_mystic_melody(state, "Melty Manor", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Bark", player),
        lambda state:
            map_mystic_melody(state, "Sub-Zero Peak", player)
            or hundred_wins(state, "Driver: Bean", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Battle Kukku XV", player),
        lambda state:
            map_mystic_melody(state, "Vermilion Vessel", player)
            or hundred_wins(state, "Driver: Tails", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Bean", player),
        lambda state:
            state.can_reach("Tinkerer's Arena", 'Region', player)
            or hundred_wins(state, "Driver: Bark", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Big", player),
        lambda state:
            state.can_reach("Emerald Coast", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Billy Hatcher", player),
        lambda state:
            state.can_reach("Joypolis", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Blaze", player),
        lambda state:
            map_time_attack(state, "Blizzard Peaks", player)
            or hundred_wins(state, "Driver: Silver", player)
    )

    # "Challenge - Driver: Bomb" is always possible

    set_rule(
        multiworld.get_location("Challenge - Driver: Carol", player),
        lambda state:
            state.can_reach("Aqua Tunnel", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Caterkiller", player),
        lambda state:
            (state.can_reach("Desert Palace", 'Region', player))
            #and state.has("Driver: Eggman", player)) # Not an individual item yet
           or hundred_wins(state, "Driver: Motobug", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Chao", player),
        lambda state:
            state.has("Follower: Chao Egg", player)
            or map_mystic_melody(state, "City Escape", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Chaos", player),
        lambda state:
            (can_reach_sealed_star(state, player))
            #and state.has("Driver: Sonic", player)) # Not an individual item yet
            or hundred_wins(state, "Driver: Tikal", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Charmy", player),
        lambda state:
            map_time_attack(state, "Isolated Island", player)
            or hundred_wins(state, "Driver: Espio", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Chuchu", player),
        lambda state:
            state.can_reach("Neon Resort", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Cluckoid", player),
        lambda state:
            state.can_reach("Tree Ring", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Cream", player),
        lambda state:
            state.can_reach("Leaf Storm", 'Region', player)
            and state.has("Driver: Blaze", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Ecco", player),
        lambda state:
            state.can_reach("Azure Axiom", 'Region', player)
    )

    # "Challenge - Driver: Eggrobo" requires Knuckles, but otherwise is always possible

    set_rule(
        multiworld.get_location("Challenge - Driver: Emerl", player),
        lambda state:
            state.can_reach("Tails Lab", 'Region', player)
    )

    # "Challenge - Driver: Espio" is always possible

    # "Challenge - Driver: Flicky" requires Motobug, but otherwise is always possible

    set_rule(
        multiworld.get_location("Challenge - Driver: Gum", player),
        lambda state:
            state.has_group("Spray Cans", player) >= 75 # 75% of spray cans
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Gutbuster", player),
        lambda state:
            state.can_reach("Sundae Drive", 'Region', player)
            and state.has("Driver: Heavy", player)
            and state.has("Driver: Bomb", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Headdy", player),
        lambda state:
            map_mystic_melody(state, "Northern District", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Heavy", player),
        lambda state:
            map_prison_break(state, "Electra Clacker", player)
            or hundred_wins(state, "Driver: Bomb", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Heavy Magician", player),
        lambda state:
            state.has_group("Drivers", player) >= 27 # 50% of drivers
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Honey", player),
        lambda state:
            state.can_reach("Death Egg's Eye", 'Region', player)
            #or map_time_attack(state, "Death Egg's Eye", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Jack Frost", player),
        lambda state:
            state.can_reach("SRB2 Frozen Night", 'Region', player)
            # Technically always possible to crash the game,
            # but we probably don't want that in logic.
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Jet", player),
        lambda state:
            state.can_reach("Sky Babylon", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Orenzo", player),
        lambda state:
            False
    )

    # "Challenge - Driver: Mail" is always possible...
    # but takes a while, so it should PROBABLY get some
    # kind of logic behind it

    set_rule(
        multiworld.get_location("Challenge - Driver: Maria", player),
        lambda state:
            map_mystic_melody(state, "Lost Colony", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Mecha Sonic", player),
        lambda state:
            state.can_reach("Sky Sanctuary", 'Region', player)
            and state.has("Gear 3 + GP Vicious Mode", player)
            #and state.has("Driver: Knuckles", player)) # Not an individual item yet
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Metal Knuckles", player),
        lambda state:
            state.has("Driver: Tails Doll", player)
            or hundred_wins(state, "Driver: Metal Sonic", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: NiGHTS", player),
        lambda state:
            map_mystic_melody(state, "Avant Garden", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Orta", player),
        lambda state:
            can_reach_sealed_star(state, player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Pulseman", player),
        lambda state:
            state.can_reach("Kodachrome Void", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Rappy", player),
        lambda state:
            state.can_reach("Las Vegas", 'Region', player)
    )

    # "Challenge - Driver: Ray" is always possible

    set_rule(
        multiworld.get_location("Challenge - Driver: Redz", player),
        lambda state:
            state.can_reach("Hidden Palace", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Rouge", player),
        lambda state:
            state.can_reach("Security Hall", 'Region', player)
            or hundred_wins(state, "Driver: Knuckles", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Sakura Shinguji", player),
        lambda state:
            state.can_reach("Hanagumi Hall", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Shadow", player),
        lambda state:
            state.can_reach("Lost Colony", 'Region', player)
            or hundred_wins(state, "Driver: Sonic", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Silver", player),
        lambda state:
            state.can_reach("Mega Collision Chaos", 'Region', player)
            or hundred_wins(state, "Driver: Blaze", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Surge", player),
        lambda state:
            map_mystic_melody(state, "Emerald Hill", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Tails Doll", player),
        lambda state:
            map_mystic_melody(state, "Regal Ruin", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Tikal", player),
        lambda state:
            map_mystic_melody(state, "Coastal Temple", player)
            or hundred_wins(state, "Driver: Chaos", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Vectorman", player),
        lambda state:
            state.can_reach("Dark Fortress", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Whisper", player),
        lambda state:
            state.can_reach("Withering Chateau", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Wonder Boy", player),
        lambda state:
            map_mystic_melody(state, "Darkvile Castle 2", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Zipp", player),
        lambda state:
            map_mystic_melody(state, "Hidden Palace", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Driver: Ring the Racer", player),
        lambda state:
            state.has("Driver: Mail", player)
            and state.can_reach("Sunbeam Paradise: Controls", 'Region', player)
    )

def create_challenges_followers_rules(multiworld: MultiWorld, player: int):
    set_rule(
        multiworld.get_location("Challenge - Follower: Motobuddy", player),
        lambda state:
            state.can_reach("Motobug Motorway", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Buzz Bomber", player),
        lambda state:
            state.can_reach("Honeycomb Hollow", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Newtron", player),
        lambda state:
            map_spb_attack(state, "Mega Green Hill", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Orbinaut", player),
        lambda state:
            can_reach_sealed_star(state, player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Jaws", player),
        lambda state:
            state.can_reach("Labyrinth", 'Region', player)
            #and state.has("Driver: Sonic", player)
    )

    # "Challenge - Follower: Bomb" is always possible

    # "Challenge - Follower: Motobricks" is always possible ... but also kind of annoying

    set_rule(
        multiworld.get_location("Challenge - Follower: Uni-Uni", player),
        lambda state:
            map_mystic_melody(state, "Star Light", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Chaos Emerald", player),
        lambda state:
            (state.can_reach("Sealed Star: Balconies", 'Region', player)
            and state.can_reach("Sealed Star: Church", 'Region', player)
            and state.can_reach("Sealed Star: Courtyard", 'Region', player)
            and state.can_reach("Sealed Star: Villa", 'Region', player)
            and state.can_reach("Sealed Star: Venice", 'Region', player)
            and state.can_reach("Sealed Star: Spikes", 'Region', player)
            and state.can_reach("Sealed Star: Fountain", 'Region', player))
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Anton", player),
        lambda state:
            state.can_reach("Palmtree Panic", 'Region', player)
    )

    # "Challenge - Follower: Mosqui" requires Amy, but otherwise is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Ga", player),
        lambda state:
            map_mystic_melody(state, "Collision Chaos", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Tonbo", player),
        lambda state:
            map_spb_attack(state, "Lavender Shrine", player)
    )

    # "Challenge - Follower: Poh-Bee" is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Bata-pyon", player),
        lambda state:
            state.can_reach("Spring Yard", 'Region', player)
    )

    # "Challenge - Follower: Kabasira" requires Metal Sonic, but otherwise is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Hotaru", player),
        lambda state:
            state.can_reach("Trap Tower", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: UFO", player),
        lambda state:
            (state.has("Driver: Silver", player) and state.can_reach("CD Special Stage 8", 'Region', player))
            or map_time_attack(state, "CD Special Stage 8", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Goddess", player),
        lambda state:
            map_time_attack(state, "Angel Arrow Classic", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Sol", player),
        lambda state:
            map_time_attack(state, "Hill Top", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Flasher", player),
        lambda state:
            state.can_reach("Mystic Cave", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Jellygnite", player),
        lambda state:
            (state.has("Encore Mode", player) and state.can_reach("Hydro City", 'Region', player))
            or map_mystic_melody(state, "Sunbeam Paradise: Controls", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Aquis", player),
        lambda state:
            map_mystic_melody(state, "Storm Rig", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Octus", player),
        lambda state:
            map_mystic_melody(state, "Rusty Rig", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Asteron", player),
        lambda state:
            state.can_reach("Hard-Boiled Stadium", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Egg Pod", player),
        lambda state:
            state.can_reach("Metropolis", 'Region', player)
            #and state.has("Driver: Eggman", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Nebula", player),
        lambda state:
            state.can_reach("Silvercloud Island", 'Region', player)
            and state.has("Follower: Tornado", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Tornado", player),
        lambda state:
            state.can_reach("Angel Island", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Meramora Jr.", player),
        lambda state:
            state.has("Driver: Caterkiller", player)
            and state.can_reach("Angel Island", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Buggernaut", player),
        lambda state:
            state.can_reach("Pestilence", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bubbles", player),
        lambda state:
            state.can_reach("Marble Garden", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Balloon", player),
        lambda state:
            state.can_reach("Carnival Night", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Barrel", player),
        lambda state:
            state.can_reach("Carnival Night", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mushmeanie", player),
        lambda state:
            (state.has("Driver: Cluckoid", player) and state.can_reach("Tree Ring", 'Region', player))
            or (map_prison_break(state, "Fungal Dimension", player))
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Technosqueek", player),
        lambda state:
            state.can_reach("Mega Flying Battery", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Chainspike", player),
        lambda state:
            state.can_reach("Death Egg", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Spikebonker", player),
        lambda state:
            state.can_reach("Death Egg", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Hyudoro", player),
        lambda state:
            state.can_reach("Mega Sandopolis", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Super Emerald", player),
        lambda state:
            (state.can_reach("Sealed Star: Balconies", 'Region', player)
            and state.can_reach("Sealed Star: Church", 'Region', player)
            and state.can_reach("Sealed Star: Courtyard", 'Region', player)
            and state.can_reach("Sealed Star: Villa", 'Region', player)
            and state.can_reach("Sealed Star: Venice", 'Region', player)
            and state.can_reach("Sealed Star: Spikes", 'Region', player)
            and state.can_reach("Sealed Star: Fountain", 'Region', player)
            and state.can_reach("Sealed Star: Gallery", 'Region', player)
            and state.can_reach("Sealed Star: Alley", 'Region', player)
            and state.can_reach("Sealed Star: Steeple", 'Region', player)
            and state.can_reach("Sealed Star: Rooftops", 'Region', player)
            and state.can_reach("Sealed Star: Roulette", 'Region', player)
            and state.can_reach("Sealed Star: Towers", 'Region', player)
            and state.can_reach("Sealed Star: Atlantis", 'Region', player))
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: S.P.B. Jr.", player),
        lambda state:
            False # TODO: logic for 777 medals
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Burboom", player),
        lambda state:
            state.has("Driver: Espio", player)
            and state.can_reach("Isolated Island", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bushbubble", player),
        lambda state:
            state.can_reach("World 1 Map", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Gotcha", player),
        lambda state:
            state.can_reach("Bigtime Breakdown", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Motorspike", player),
        lambda state:
            state.has("Driver: Charmy", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Piranhy", player),
        lambda state:
            map_mystic_melody(state, "Sunbeam Paradise: Rings", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Ticktock", player),
        lambda state:
            map_time_attack(state, "Joypolis", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Scouter", player),
        lambda state:
            state.can_reach("Gems Museum", 'Region', player)
            #and state.has("Driver: Motobug", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Snowman", player),
        lambda state:
            state.can_reach("Blue Mountain 2", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Firefly", player),
        lambda state:
            state.has("Driver: Flicky", player)
            and state.can_reach("SEGA Saturn", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Whirl", player),
        lambda state:
            state.can_reach("Gust Planet", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mecha Hiyoko", player),
        lambda state:
            state.can_reach("Aqueduct Crystal", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Silver Sonic", player),
        lambda state:
            map_spb_attack(state, "Chaos Chute", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Frogger", player),
        lambda state:
            state.has("Driver: Big", player)
            and state.has("Follower: Froggy", player)
            and state.can_reach("Wood", 'Region', player)
    )

    # "Challenge - Follower: Bombaberry" is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Spidal Tap", player),
        lambda state:
            state.can_reach("Robotnik Winter", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bomblur", player),
        lambda state:
            state.has("Gear 3 + GP Vicious Mode", player)
            and state.can_reach("Turquoise Hill", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mukaka", player),
        lambda state:
            state.has("Driver: Vectorman", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Sandoom", player),
        lambda state:
            state.can_reach("Roasted Ruins", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Gaikoko", player),
        lambda state:
            map_mystic_melody(state, "Haunted Ship", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Chao", player),
        lambda state:
            state.has("Follower: Chao Egg", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Chao Egg", player),
        lambda state:
            state.can_reach("Barrier Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Froggy", player),
        lambda state:
            state.can_reach("Emerald Coast", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Spinner", player),
        lambda state:
            state.can_reach("Speed Highway", 'Region', player)
            #and state.has("Driver: Sonic", player)
    )

    # "Challenge - Follower: Kart Kiki" requires Metal Sonic, but otherwise is always possible
    # "Challenge - Follower: Bowling Pin" is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Hint Orb", player),
        lambda state:
            can_reach_sealed_star(state, player)
            and state.has("Driver: Tikal", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Jet Booster", player),
        lambda state:
            state.can_reach("Hot Shelter", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Chaclon", player),
        lambda state:
            (state.has("GP Master Mode", player)
            and state.can_reach("Pico Park", 'Region', player))
            # TODO: or 200 medals
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Hero Chao", player),
        lambda state:
            state.has("Follower: Chao", player)
            #and state.has("Driver: Sonic", player)
            and state.can_reach("Hero Chao Garden", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Dark Chao", player),
        lambda state:
            state.has("Follower: Chao", player)
            and state.has("Driver: Shadow", player)
            and state.can_reach("Dark Chao Garden", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mono Beetle", player),
        lambda state:
            state.can_reach("City Escape", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Gold Beetle", player),
        lambda state:
            state.can_reach("City Escape", 'Region', player)
    )

    # "Challenge - Follower: Attack Boo" is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Boo", player),
        lambda state:
            state.has("Driver: Rogue", player)
            and state.can_reach("Darkvile Castle 1", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Chaos Drive", player),
        lambda state:
            can_reach_sealed_star(state, player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Emerald Radar", player),
        lambda state:
            state.can_reach("Meteor Herd", 'Region', player)
            #and state.has("Driver: Knuckles", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mystic Melody", player),
        lambda state:
            state.can_reach("Lost Colony", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Cheese", player),
        lambda state:
            state.has("Driver: Cream", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Egg Flapper", player),
        lambda state:
            map_prison_break(state, "Power Plant", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Klagen", player),
        lambda state:
            state.can_reach("Water Palace", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Gold Klagen", player),
        lambda state:
            map_time_attack(state, "Water Palace", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Hermit Crab", player),
        lambda state:
            state.can_reach("Sunbeam Paradise: Brakes", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Splats", player),
        lambda state:
            map_mystic_melody(state, "Press Garden", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Marble UAP", player),
        lambda state:
            map_prison_break(state, "Mega Marble", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Claw Guy", player),
        lambda state:
            state.can_reach("Advent Angel", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bubbler's Mother", player),
        lambda state:
            map_spb_attack(state, "Chemical Facility", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Spinpole", player),
        lambda state:
            state.can_reach("Vermilion Vessel", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Flysquid", player),
        lambda state:
            state.can_reach("Hydro Plant", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Final Duck", player),
        lambda state:
            state.has("Driver: Billy Hatcher", player)
            and state.can_reach("Kodachrome Void", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Tridrill", player),
        lambda state:
            state.has("Gear 3 + GP Vicious Mode", player)
            and state.can_reach("Rumble Ridge", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Cappy", player),
        lambda state:
            state.has("Gear 3 + GP Vicious Mode", player)
            and state.can_reach("Recycle Cup B", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Jetarang", player),
        lambda state:
            state.can_reach("Recycle Cup A", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Balldron", player),
        lambda state:
            state.has("Driver: Metal Knuckles", player)
            and state.can_reach("Crimson Core", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bomber", player),
        lambda state:
            state.has("Gear 3 + GP Vicious Mode", player)
            and state.can_reach("Ice Paradise", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Gyro", player),
        lambda state:
            state.can_reach("Gravtech Dimension", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: SRB1 Crawla", player),
        lambda state:
            state.has("Gear 3 + GP Vicious Mode", player)
            and state.can_reach("SRB2 Frozen Night", 'Region', player)
            # TODO: Once starting drivers are separated, there should be driver logic here...
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: GuardRobo", player),
        lambda state:
            map_mystic_melody(state, "Technology Tundra", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: HotRobo", player),
        lambda state:
            state.can_reach("Mega Lava Reef", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Pyrex", player),
        lambda state:
            state.can_reach("Mega Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Spybot 2000", player),
        lambda state:
            state.can_reach("Thunder Piston", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: SRB2 Crawla", player),
        lambda state:
            state.has("Driver: Bomb", player)
            and state.can_reach("SRB2 Meadow Match", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mean Bean", player),
        lambda state:
            state.has("Follower: Has Bean", player)
            #and state.has("Driver: Eggman", player)
            and state.can_reach("Egg Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: C.H.R.O.M.E.", player),
        lambda state:
            state.can_reach("Virtual Highway", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Tridentz", player),
        lambda state:
            state.can_reach("Nova Shore", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Stegospike", player),
        lambda state:
            state.has("Driver: Redz", player)
            and state.can_reach("Bronze Lake", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Flicky Turncoat", player),
        lambda state:
            state.has("Driver: Flicky", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Manegg", player),
        lambda state:
            map_mystic_melody(state, "Nova Shore", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Blend Eye", player),
        lambda state:
            state.can_reach("Espresso Lane", 'Region', player) # Adventure Example doesn't have a region yet; it doesn't seem super necessary
    )

    # "Challenge - Follower: Flicky" is always possible

    set_rule(
        multiworld.get_location("Challenge - Follower: Red Flicky", player),
        lambda state:
            state.can_reach("Scarlet Gardens", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Pink Flicky", player),
        lambda state:
            state.can_reach("Diamond Dust", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Green Flicky", player),
        lambda state:
            state.can_reach("Regal Ruin", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Clucky", player),
        lambda state:
            state.has("Driver: Cluckoid", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Fish", player),
        lambda state:
            state.can_reach("Mega Aqua Lake", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Puffin", player),
        lambda state:
            state.can_reach("Sub-Zero Peak", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Dove", player),
        lambda state:
            state.can_reach("Flash Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Canary", player),
        lambda state:
            state.can_reach("Endless Mine 1", 'Region', player)
            # TODO: Might need logic for a list of drivers
            # that can can more easily make Cluckoid retire
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bat", player),
        lambda state:
            state.can_reach("Darkvile Castle 2", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Has Bean", player),
        lambda state:
            state.has("Driver: Arle", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Nomi", player),
        lambda state:
            state.has("Driver: Arle", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Glyph", player),
        lambda state:
            state.has("Driver: Ecco", player)
            and state.can_reach("Crystal Island", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Asterite", player),
        lambda state:
            map_mystic_melody(state, "Azure Axiom", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Controller", player),
        lambda state:
            state.has("GP Master Mode", player)
            and (state.can_reach("Sealed Star: Balconies", 'Region', player)
            and state.can_reach("Sealed Star: Church", 'Region', player)
            and state.can_reach("Sealed Star: Courtyard", 'Region', player)
            and state.can_reach("Sealed Star: Villa", 'Region', player)
            and state.can_reach("Sealed Star: Venice", 'Region', player)
            and state.can_reach("Sealed Star: Spikes", 'Region', player)
            and state.can_reach("Sealed Star: Fountain", 'Region', player)
            and state.can_reach("Sealed Star: Gallery", 'Region', player)
            and state.can_reach("Sealed Star: Alley", 'Region', player)
            and state.can_reach("Sealed Star: Steeple", 'Region', player)
            and state.can_reach("Sealed Star: Rooftops", 'Region', player)
            and state.can_reach("Sealed Star: Roulette", 'Region', player)
            and state.can_reach("Sealed Star: Towers", 'Region', player)
            and state.can_reach("Sealed Star: Atlantis", 'Region', player))
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Orblet", player),
        lambda state:
            (state.has("Driver: AiAi", player)
            and state.has("Driver: Aigis", player)
            and state.has("Driver: Arle", player)
            and state.has("Driver: Azusa Miura", player)
            and state.has("Driver: Billy Hatcher", player)
            and state.has("Driver: Carol", player)
            and state.has("Driver: Chuchu", player)
            and state.has("Driver: Ecco", player)
            and state.has("Driver: Gum", player)
            and state.has("Driver: Headdy", player)
            and state.has("Driver: Jack Frost", player)
            and state.has("Driver: Mail", player)
            and state.has("Driver: NiGHTS", player)
            and state.has("Driver: Orta", player)
            and state.has("Driver: Pulseman", player)
            and state.has("Driver: Rappy", player)
            and state.has("Driver: Sakura Shinguji", player)
            and state.has("Driver: Vectorman", player)
            and state.has("Driver: Wonder Boy", player))
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Kobu", player),
        lambda state:
            state.can_reach("Hanagumi Hall", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: The Cake From Hell", player),
        lambda state:
            state.has("Driver: Gutbuster", player)
            and state.can_reach("Spring Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Billiards Cactus", player),
        lambda state:
            state.has("Driver: AiAi", player)
            and state.can_reach("Mirage Saloon", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Mag", player),
        lambda state:
            state.can_reach("Las Vegas", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Bacura", player),
        lambda state:
            map_prison_break(state, "Media Studio", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Cacodemon", player),
        lambda state:
            map_prison_break(state, "Dead Simple", player)
    )

    set_rule(
        multiworld.get_location("Challenge - Follower: Shade Core", player),
        lambda state:
            state.has("Driver: Carol", player)
            and state.can_reach("Aqua Tunnel", 'Region', player)
    )

access_item_to_can_count = {
    "Ring Cup Access": 5,
    "Sneaker Cup Access": 5,
    "Spring Cup Access": 5,
    "Barrier Cup Access": 5,
    "Invincible Cup Access": 5,
    "Emerald Cup Access": 5, # 6 if counting Hidden Palace
    "Extra Cup Access": 5,

    "S.P.B. Cup Access": 5,
    "Rocket Cup Access": 5,
    "Aqua Cup Access": 5,
    "Lightning Cup Access": 5,
    "Flame Cup Access": 5,
    "Super Cup Access": 5,
    "Egg Cup Access": 4, # 5 if Milky Way gets added

    "Goggles Cup Access": 5,
    "Timer Cup Access": 5,
    "Grow Cup Access": 5,
    "Chao Cup Access": 5,
    "Wing Cup Access": 5,
    "Mega Cup Access": 5,
    "Phantom Cup Access": 5,

    "Flash Cup Access": 5,
    "Swap Cup Access": 5,
    "Shrink Cup Access": 5,
    "Bomb Cup Access": 5,
    "Power Cup Access": 5,
    "Genesis Cup Access": 5,
    "Skate Cup Access": 5,

    "Recycle Cup A Access": 5,
    "Recycle Cup B Access": 5,

    "Test Run Access": 0,
    "Hidden Palace Access": 1,
    "Test Track Access": 1,
}

def enough_accessible_cans(state: CollectionState, required_cans: int, player: int):
    total_cans = 0

    for item in sorted(Items.item_groups["Cups"]):
        if (state.has(item, player)):
            total_cans += access_item_to_can_count[item]

    for item in sorted(Items.item_groups["Levels"]):
        if (state.has(item, player)):
            total_cans += access_item_to_can_count[item]

    return (total_cans >= required_cans)

def create_challenges_spraycan_rules(multiworld: MultiWorld, player: int):
    can_number = 0
    sorted_spraycans = dict(sorted(Locations.challenges_spraycans_locations.items(), key = lambda item: item[1]))
    for location_name in sorted(sorted_spraycans):
        can_number += 1
        set_rule(
            multiworld.get_location(location_name, player),
            lambda state:
                enough_accessible_cans(state, can_number, player)
        )


def create_challenges_cups_rules(multiworld: MultiWorld, player: int):
    # "Challenge - Ring Cup" can always be done

    # 1-1 cup challenges: beat previous cup
    set_rule(
        multiworld.get_location("Challenge - Sneaker Cup", player),
        lambda state:
            state.can_reach("Ring Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Spring Cup", player),
        lambda state:
            state.can_reach("Sneaker Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Barrier Cup", player),
        lambda state:
            state.can_reach("Spring Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Invincible Cup", player),
        lambda state:
            state.can_reach("Barrier Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Emerald Cup", player),
        lambda state:
            state.can_reach("Invincible Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Extra Cup", player),
        lambda state:
            state.can_reach("Emerald Cup", 'Region', player)
    )

    # 1-2 cup challenges: beat Extra cup
    set_rule(
        multiworld.get_location("Challenge - S.P.B. Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Rocket Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Aqua Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Lightning Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Flame Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Super Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    # egg cup challenge: beat all previous cups
    set_rule(
        multiworld.get_location("Challenge - Egg Cup", player),
        lambda state:
            (state.can_reach("Ring Cup", 'Region', player)
            and state.can_reach("Sneaker Cup", 'Region', player)
            and state.can_reach("Spring Cup", 'Region', player)
            and state.can_reach("Barrier Cup", 'Region', player)
            and state.can_reach("Invincible Cup", 'Region', player)
            and state.can_reach("Emerald Cup", 'Region', player)
            and state.can_reach("Extra Cup", 'Region', player)
            and state.can_reach("S.P.B. Cup", 'Region', player)
            and state.can_reach("Rocket Cup", 'Region', player)
            and state.can_reach("Aqua Cup", 'Region', player)
            and state.can_reach("Lightning Cup", 'Region', player)
            and state.can_reach("Flame Cup", 'Region', player)
            and state.can_reach("Super Cup", 'Region', player))
    )

    # page 2 cup challenges: beat all previous cups OR get chaos emerald on previous page's corresponding cup
    # because you can always get the chaos emerald, the logic is for the chaos emerald
    set_rule(
        multiworld.get_location("Challenge - Goggles Cup", player),
        lambda state:
            state.can_reach("Ring Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Timer Cup", player),
        lambda state:
            state.can_reach("Sneaker Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Grow Cup", player),
        lambda state:
            state.can_reach("Spring Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Chao Cup", player),
        lambda state:
            state.can_reach("Barrier Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Wing Cup", player),
        lambda state:
            state.can_reach("Invincible Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Mega Cup", player),
        lambda state:
            state.can_reach("Emerald Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Phantom Cup", player),
        lambda state:
            state.can_reach("Extra Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Flash Cup", player),
        lambda state:
            state.can_reach("S.P.B. Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Swap Cup", player),
        lambda state:
            state.can_reach("Rocket Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Shrink Cup", player),
        lambda state:
            state.can_reach("Aqua Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Bomb Cup", player),
        lambda state:
            state.can_reach("Lightning Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Power Cup", player),
        lambda state:
            state.can_reach("Flame Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Genesis Cup", player),
        lambda state:
            state.can_reach("Super Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Skate Cup", player),
        lambda state:
            state.can_reach("Egg Cup", 'Region', player)
    )

    # page 3 cup challenges: beat the last row's cups with the Chaos Emerald
    set_rule(
        multiworld.get_location("Challenge - Recycle Cup A", player),
        lambda state:
            state.can_reach("Phantom Cup", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Recycle Cup B", player),
        lambda state:
            state.can_reach("Skate Cup", 'Region', player)
    )

def create_challenges_misc_rules(multiworld: MultiWorld, player: int):
    # "Challenge - Prison Break Mode" can always be done

    set_rule(
        multiworld.get_location("Challenge - Special Mode", player),
        lambda state:
            state.can_reach("Sealed Star: Balconies", 'Region', player)
            and state.can_reach("Sealed Star: Church", 'Region', player)
            and state.can_reach("Sealed Star: Courtyard", 'Region', player)
            and state.can_reach("Sealed Star: Villa", 'Region', player)
            and state.can_reach("Sealed Star: Venice", 'Region', player)
            and state.can_reach("Sealed Star: Spikes", 'Region', player)
            and state.can_reach("Sealed Star: Fountain", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Gear 3 + GP Vicious Mode", player),
        lambda state:
            state.can_reach("Egg Cup", 'Region', player)
    )

    # "Challenge - Time Attack Mode" can always be done

    # "Challenge - GP Master Mode" can always be done

    set_rule(
        multiworld.get_location("Challenge - GP Master Mode", player),
        lambda state:
            state.can_reach("Sealed Star: Balconies", 'Region', player)
            and state.can_reach("Sealed Star: Church", 'Region', player)
            and state.can_reach("Sealed Star: Courtyard", 'Region', player)
            and state.can_reach("Sealed Star: Villa", 'Region', player)
            and state.can_reach("Sealed Star: Venice", 'Region', player)
            and state.can_reach("Sealed Star: Spikes", 'Region', player)
            and state.can_reach("Sealed Star: Fountain", 'Region', player)
            and state.can_reach("Sealed Star: Gallery", 'Region', player)
            and state.can_reach("Sealed Star: Alley", 'Region', player)
            and state.can_reach("Sealed Star: Steeple", 'Region', player)
            and state.can_reach("Sealed Star: Rooftops", 'Region', player)
            and state.can_reach("Sealed Star: Roulette", 'Region', player)
            and state.can_reach("Sealed Star: Towers", 'Region', player)
            and state.can_reach("Sealed Star: Atlantis", 'Region', player)
    )

    set_rule(
        multiworld.get_location("Challenge - Encore Mode", player),
        lambda state:
            have_all_cups(state, player)
    )

    set_rule(
        multiworld.get_location("Challenge - SPB Attack Mode", player),
        lambda state:
            state.has("Encore Mode", player)
            and state.has("Time Attack Mode", player)
            # TODO: 500 medals check
    )

    # "Challenge - Online Play" can always be done

    # "Challenge - Alternate Titlescreen" can always be done

    # "Challenge - Egg TV" can always be done

    set_rule(
        multiworld.get_location("Challenge - Sound Test", player),
        lambda state:
            state.has_group("Alt. Music", player) >= 13 # 25% of alt music
    )

    # "Challenge - Playing with Addons" can always be done

    # Lost & Found levels
    set_rule(
        multiworld.get_location("Challenge - Lost & Found: Test Run", player),
        lambda state:
            have_all_levels_but_test_run(state, player)
    )

    set_rule(
        multiworld.get_location("Challenge - Lost & Found: Hidden Palace", player),
        lambda state:
            state.can_reach("Mystic Cave", 'Region', player)
    )

    # "Challenge - Lost & Found: Test Track" can always be done

def enough_accessible_cds(state: CollectionState, required_cds: int, player: int):
    total_cds = 0

    for item in sorted(Items.item_groups["Cups"]):
        if (state.has(item, player)):
            total_cds += 2

    return False

def create_challenges_cd_rules(multiworld: MultiWorld, player: int):
    # CDs CAN just be grinded over and over and over on a single level, but
    # require levels be unlocked over time, so that grinding is out of logic.
    cd_number = 0
    sorted_cds = dict(sorted(Locations.challenges_cd_locations.items(), key = lambda item: item[1]))
    for location_name in sorted(sorted_cds):
        cd_number += 1
        set_rule(
            multiworld.get_location(location_name, player),
            lambda state:
                enough_accessible_cds(state, cd_number, player)
        )

def create_challenges_rules(multiworld: MultiWorld, player: int):
    create_challenges_drivers_rules(multiworld, player)
    create_challenges_followers_rules(multiworld, player)
    create_challenges_spraycan_rules(multiworld, player)
    create_challenges_cups_rules(multiworld, player)
    create_challenges_misc_rules(multiworld, player)
    create_challenges_cd_rules(multiworld, player)

def create_rules(multiworld: MultiWorld, player: int):
    create_challenges_rules(multiworld, player)
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
