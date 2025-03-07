from dataclasses import dataclass, field
from enum import Enum


@dataclass
class CreatureDataMixin:
    size: str
    legs: int
    tail: bool = field(repr=False, default=True)


class Creature(CreatureDataMixin, Enum):
    BEETLE = 'small', 6
    DOG = 'medium', 4


# you can now access the dataclass fields on the enumeration values
# as with enum properties:
assert Creature.BEETLE.size == 'small'
assert Creature.BEETLE.legs == 6
assert Creature.BEETLE.tail is True
