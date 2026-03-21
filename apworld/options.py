from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, DefaultOnToggle, Choice, Range, NamedRange, OptionGroup


class CharWinsCount(NamedRange):
    """
    Alter the number of wins required for any "100 wins playing as X" challenges.

    - **Default**: Require only 5 wins per character.
    - **Exclude**: Require 100 wins per character, but exclude from logic. Every challenge that has this condition uses it as an alternative, so this doesn't remove any locations.
    - **Vanilla**: Require 100 wins per character, in logic. Not recommended.
    """

    internal_name = "character_wins_count"
    display_name = "Character Wins Count"
    range_start = 1
    range_end = 100
    default = 5
    special_range_names = {
        "default": 5,
        "vanilla": 100,
        "exclude": 0,
    }


class SimpleMapAccess(DefaultOnToggle):
    """
    If enabled, then maps are available on level select as soon as their respective Cup / Map Access item is found.
    If disabled, then it's required to visit the map first, like the vanilla game.
    This option has the most noticeable effect on Lost & Found maps.
    """

    internal_name = "simple_map_access"
    display_name = "Simplify Map Access"


@dataclass
class RingRacersOptions(PerGameCommonOptions):
    character_wins_count: CharWinsCount
    simple_map_access: SimpleMapAccess
