import typing as t
from dataclasses import dataclass, field
from enum_properties import EnumProperties, Symmetric


@dataclass
class CreatureDataMixin:
    size: str
    legs: int
    tail: bool = field(repr=False, default=True)


class Creature(CreatureDataMixin, EnumProperties):

    kingdom: t.Annotated[str, Symmetric()]

    BEETLE = 'small', 6, False, 'insect'
    DOG = 'medium', 4, 'animal'


# you can now access the dataclass fields on the enumeration values
# as with enum properties:
assert Creature.BEETLE.size == 'small'
assert Creature.BEETLE.legs == 6
assert Creature.BEETLE.tail is False
assert Creature.BEETLE.kingdom == 'insect'

# adding symmetric properties onto a dataclass enum can help with
# marshalling external data into the enum classes!
assert Creature('insect') is Creature.BEETLE
