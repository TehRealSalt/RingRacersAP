from dataclasses import dataclass

from Options import PerGameCommonOptions, ItemsAccessibility, Toggle, DefaultOnToggle, Choice, Range, NamedRange, Visibility, OptionGroup


class StartingDriverCount(Range):
    """
    How many drivers to start with.
    """

    internal_name = "starting_driver_count"
    display_name = "Starting Driver Count"
    range_start = 1
    range_end = 9
    default = 9


class StartingDriverPool(Choice):
    """
    Determine the pool that is chosen from when randomizing starting drivers.

    - **Vanilla**: Randomize from only the starting drivers.
    - **Balanced**: Randomize from any drivers, but require at least one from each engine class.
    - **Full**: Randomize from any drivers, no restrictions.
    """

    internal_name = "starting_driver_pool"
    display_name = "Starting Driver Pool"
    option_vanilla = 0
    option_balanced = 1
    option_full = 2
    default = 1


class CharWinsCount(NamedRange):
    """
    Alter the number of wins required for any "100 wins playing as X" challenges.

    - **Exclude**: Require 100 wins per character, but exclude from logic. Every challenge that has this condition uses it as an alternative, so this doesn't remove any locations.
    - **Nerfed**: Require only 5 wins per character, in logic.
    - **Vanilla**: Require 100 wins per character, in logic. Not recommended.
    """

    internal_name = "character_wins_count"
    display_name = "Character Wins Count"
    range_start = 1
    range_end = 100
    default = 0
    special_range_names = {
        "exclude": 0,
        "nerfed": 5,
        "vanilla": 100,
    }


class SimpleMapAccess(DefaultOnToggle):
    """
    If enabled, then maps are available on level select as soon as their respective Cup / Map Access item is found.
    If disabled, then it's required to visit the map first, like the vanilla game.
    This option has the most noticeable effect on Lost & Found maps.
    """

    internal_name = "simple_map_access"
    display_name = "Simplify Map Access"


class GoalNumTrophies(Range):
    """
    How many Cup trophies are needed in order to complete the game.
    """

    internal_name = "goal_num_trophies"
    display_name = "# of Required Trophies"
    range_start = 1
    range_end = 30
    default = 14


class GoalTrophyLevel(NamedRange):
    """
    The final placement needed in order to for a Cup's trophy to be considered for goal.
    """

    internal_name = "goal_trophy_level"
    display_name = "Required Trophy Placement"
    range_start = 1
    range_end = 3
    default = 0
    special_range_names = {
        "any": 0,
        "gold": 1,
        "silver": 2,
        "bronze": 3,
    }


class Challenges(DefaultOnToggle):
    """
    Include most locations from the vanilla "Challenges" menu.
    """

    internal_name = "challenges"
    display_name = "Challenges Board"


class SprayCans(DefaultOnToggle):
    """
    Include each map's Spray Can as a location.
    """

    internal_name = "spray_cans"
    display_name = "Spray Cans"


class PrisonEggCDs(Toggle):
    """
    Include the Prison Egg CD milestones as locations.

    Grinding is possible, but shouldn't be necessary as logic only expects that you get one CD per Bonus Round that has been unlocked.
    However, missing a CD will require replaying part of a Grand Prix. Enable at your own risk!
    """

    internal_name = "prison_egg_cds"
    display_name = "Prison Egg CDs"


class GumChallenge(Toggle):
    """
    Forcefully include Gum's Challenge. Does nothing if Challenges are off.
    
    This will turn many Spray Cans from filler into progression items, only for a single check. Enable at your own risk!
    """

    internal_name = "gum_challenge"
    display_name = "Gum's Challenge"


class SoundTestChallenge(Toggle):
    """
    Include Sound Test's Challenge. Does nothing if Challenges are off.
    
    This will turn some Alt. Music from filler into progression items, only for a single check. Enable at your own risk!
    """

    internal_name = "sound_test_challenge"
    display_name = "Sound Test's Challenge"


class ProgressiveCups(NamedRange):
    """
    The number of cup unlocks that are progressive.
    The remaining cups are unlocked individually.
    """

    visibility = Visibility.spoiler # WIP

    internal_name = "progressive_cups"
    display_name = "# of Progressive Cups"
    range_start = 1
    range_end = 30
    default = 0
    special_range_names = {
        "off": 0,
    }


class ChaoKeyRatio(Range):
    """
    Replace some filler items with Chao Keys, as a percentage of the total number of enabled locations.

    If there are enough locations for KKD Honors to spawn, then those will be replaced first.
    Otherwise, this replaces unique filler items, until either the quota is met or all filler is replaced.
    """

    internal_name = "chao_key_ratio"
    display_name = "Chao Key %"
    range_start = 0
    range_end = 100
    default = 10


class KeygenRate(NamedRange):
    """
    How many rounds need to be completed for a Chao Key to be generated.

    Disabling will cause Chao Keys to only be found from checks, or not at all if "Chao Key %" is zero.
    """

    internal_name = "keygen_rate"
    display_name = "KEYGEN Rate"
    range_start = 1
    range_end = 32
    default = 5
    special_range_names = {
        "disabled": 0,
    }


@dataclass
class RingRacersOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility

    challenges: Challenges
    spray_cans: SprayCans
    prison_egg_cds: PrisonEggCDs
    gum_challenge: GumChallenge
    sound_test_challenge: SoundTestChallenge

    goal_num_trophies: GoalNumTrophies
    goal_trophy_level: GoalTrophyLevel

    starting_driver_pool: StartingDriverPool
    starting_driver_count: StartingDriverCount

    chao_key_ratio: ChaoKeyRatio
    keygen_rate: KeygenRate

    character_wins_count: CharWinsCount
    simple_map_access: SimpleMapAccess

    progressive_cups: ProgressiveCups


option_groups = [
    OptionGroup(
        "Locations",
        [Challenges, SprayCans, PrisonEggCDs, GumChallenge, SoundTestChallenge],
    ),
    OptionGroup(
        "Goal Options",
        [GoalNumTrophies, GoalTrophyLevel],
    ),
    OptionGroup(
        "Starting Drivers",
        [StartingDriverPool, StartingDriverCount],
    ),
    OptionGroup(
        "Chao Keys",
        [ChaoKeyRatio, KeygenRate],
    ),
    OptionGroup(
        "Logic",
        [CharWinsCount, SimpleMapAccess],
    ),
]
