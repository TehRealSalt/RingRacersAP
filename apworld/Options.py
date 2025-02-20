import typing
from dataclasses import dataclass
from Options import Option, Choice, Range, Toggle, DefaultOnToggle, PerGameCommonOptions

class Goal(Choice):
    """
    Determines the goal of the seed
    
    Cups: Complete a certain number of Cups in Grand Prix mode.
    
    Emeralds: Complete a certain number of Sealed Stars in Grand Prix mode.
    
    Medals: Grab a certain number of Medals in Time Attack mode.
    
    Emblem Hunt: Collect a certain number of emblem items
    """
    display_name = "Goal"
    option_cups = 0
    option_emeralds = 1
    option_medals = 2
    option_emblem_hunt = 3
    default = 0

class TotalCups(Range):
    """
    Determines the number of Progressive Cup Unlock items are in the pool
    """
    display_name = "Total Cups"
    range_start = 1
    range_end = 30
    default = 30

class RequiredCups(Range):
    """
    Determines the number of cups that must be 
    """
    display_name = "Total Cups"
    range_start = 1
    range_end = 30
    default = 65

class CupTrophyRequirement(Choice):
    """
    The minimum placement required to get the trophy check for completing a Cup.
    """
    display_name = "Required Trophy for Cup"
    option_none = -1
    option_fourth = 0
    option_third = 1
    option_second = 2
    option_first = 3
    default = 0

class CupRankRequirement(Choice):
    """
    The minimum rank required to get the rank check for completing a Cup.
    """
    display_name = "Required Rank for Cup"
    option_none = -1
    option_e = 0
    option_d = 1
    option_c = 2
    option_b = 3
    option_a = 4
    option_s = 5
    default = 0

class LevelRankRequirement(Choice):
    """
    Determines the minimum rank required to get the rank check for completing a Race / Prison Break.
    """
    display_name = "Required Rank for Level"
    option_none = -1
    option_e = 0
    option_d = 1
    option_c = 2
    option_b = 3
    option_a = 4
    default = 0

class CharacterTiles(DefaultOnToggle):
    """
    Determines how characters are randomized
    
    Off: Character challenge tiles have filler items, all characters are unlocked at the start
    
    On: Character challenge tiles grant checks, only one character is unlocked at the start
    """
    display_name = "Character Randomization"

class FollowerTiles(Toggle):
    """
    Determines how Spray Cans are randomized
    
    Off: Follower challenge tiles have filler items, all followers are unlocked at the start
    
    On: Follower challenge tiles grant checks, no followers are unlocked at the start
    """
    display_name = "Spray Can Randomization"

class SprayCanTiles(Toggle):
    """
    Determines how Spray Cans are randomized
    
    Off: Spray Can challenge tiles have filler items, all colors are unlocked at the start
    
    On: Spray Can challenge tiles grant checks, only one color is unlocked at the start
    """
    display_name = "Spray Can Randomization"


class ChaoKeyPercent(Range):
    """
    How many Chao Keys to attempt to add to the pool.
    
    This is as a percentage of total challenge tile locations.

    If fewer available locations exist in the pool than this number, the number of available locations will be used instead.
    """
    display_name = "Chao Key Percentage"
    range_start = 0
    range_end = 500
    default = 65

class KeyGen(Toggle):
    """
    Chao Keys are generated by completing matches, like the vanilla game.
    """
    display_name = "Allow KEYGEN"

class ObscureLocations(Toggle):
    """
    Allow obscure / long secrets in the location pool. (Ring the Racer, Adventure Example, Hidden Palace)
    """
    display_name = "Allow Obscure Locations"

@dataclass
class RingRacersOptions(PerGameCommonOptions):
    goal: Goal
    obscure_locations: ObscureLocations
