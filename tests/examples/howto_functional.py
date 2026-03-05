import typing as t
from enum_properties import EnumProperties, IntEnumProperties, FlagProperties, p, s


# The functional API lets you build enumeration classes dynamically at runtime.
# Pass a ``properties`` argument with the member definitions to name the properties.
# String entries become plain (non-symmetric) properties; p() and s() types give
# more control, including symmetry.

Color = EnumProperties(
    'Color',
    {
        'RED':   (1, 'Roja',  'ff0000'),
        'GREEN': (2, 'Verde', '00ff00'),
        'BLUE':  (3, 'Azul',  '0000ff'),
    },
    properties=('spanish', s('hex', case_fold=True)),
)

assert Color.RED.spanish == 'Roja'
assert Color.RED.hex == 'ff0000'

# hex is symmetric – look up by hex string (case-insensitive)
assert Color('ff0000') is Color.RED
assert Color('FF0000') is Color.RED
assert Color('00ff00') is Color.GREEN


# FlagProperties also supports the functional API.

Perm = FlagProperties(
    'Perm',
    {
        'R':   (1, 'read'),
        'W':   (2, 'write'),
        'X':   (4, 'execute'),
        'RWX': (7, 'all'),
    },
    properties=(s('label', case_fold=True),),
)

assert Perm.R.label == 'read'
assert Perm('READ') is Perm.R
assert (Perm.R | Perm.W | Perm.X) is Perm.RWX
assert Perm.RWX.flagged == [Perm.R, Perm.W, Perm.X]
