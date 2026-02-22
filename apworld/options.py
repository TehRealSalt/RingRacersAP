from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class TrapChance(Range):
    """
    Percentage chance that any given Confetti Cannon will be replaced by a Math Trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


@dataclass
class RingRacersOptions(PerGameCommonOptions):
    trap_chance: TrapChance
