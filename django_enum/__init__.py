r"""

    ____    _                            ______
   / __ \  (_)___ _____  ____ _____     / ____/___  __  ______ ___
  / / / / / / __ `/ __ \/ __ `/ __ \   / __/ / __ \/ / / / __ `__ \
 / /_/ / / / /_/ / / / / /_/ / /_/ /  / /___/ / / / /_/ / / / / / /
/_____/_/ /\__,_/_/ /_/\__, /\____/  /_____/_/ /_/\__,_/_/ /_/ /_/
     /___/            /____/

"""
from django_enum.base import (
    TextChoices,
    IntegerChoices,
    FloatChoices,
    p
)
from django_enum.fields import EnumField
from django_enum.mixins import SymmetricMixin

VERSION = (1, 0, 0)

__title__ = 'Django Enum'
__version__ = '.'.join(str(i) for i in VERSION)
__author__ = 'Brian Kohan'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Brian Kohan'
