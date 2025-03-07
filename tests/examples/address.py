import typing as t
from enum_properties import EnumProperties as Enum, Symmetric


class AddressRoute(Enum):

    # name is a builtin property of Enum, we can override its case insensitivity
    name: t.Annotated[str, Symmetric(case_fold=True)]

    abbr: t.Annotated[str, Symmetric(case_fold=True)]
    alt: t.Annotated[t.List[str], Symmetric(case_fold=True)]

    # name  value    abbr         alt
    ALLEY   = 1,    'ALY', ['ALLEE', 'ALLY']
    AVENUE  = 2,    'AVE', ['AV', 'AVEN', 'AVENU', 'AVN', 'AVNUE']
    CIRCLE  = 3,    'CIR', ['CIRC', 'CIRCL', 'CRCL', 'CRCLE']

    # ... other types elided for brevity


assert (
    AddressRoute('avenue')  # the name is case insensitive and symmetric
    is
    AddressRoute('AVE')  # the abbr property is also symmetric
    is
    AddressRoute('Aven')  # values in the alt property are symmetric
    is
    AddressRoute.AVENUE  # all of the above resolve to the same enum instance
)
