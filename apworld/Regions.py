from BaseClasses import MultiWorld, Region, Location, ItemClassification
from .Locations import challenge_locations_table, RingRacersLocation
from .Items import RingRacersItem

def create_regions(multiworld: MultiWorld, player: int):
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    challenge_grid_region = Region("Challenge Grid", player, multiworld)
    challenge_grid_region.add_locations(challenge_locations_table, RingRacersLocation)
    multiworld.regions.append(challenge_grid_region)

    menu_region.connect(challenge_grid_region)

    # TEMP
    victory_location = RingRacersLocation(player, "Victory", None, challenge_grid_region)
    victory_location.place_locked_item(RingRacersItem("Victory", ItemClassification.progression, None, player))
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
    challenge_grid_region.locations.append(victory_location)
