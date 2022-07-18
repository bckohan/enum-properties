r"""

   ____                  ___                        __  _
  / __/__  __ ____ _    / _ \_______  ___  ___ ____/ /_(_)__ ___
 / _// _ \/ // /  ' \  / ___/ __/ _ \/ _ \/ -_) __/ __/ / -_|_-<
/___/_//_/\_,_/_/_/_/ /_/  /_/  \___/ .__/\__/_/  \__/_/\__/___/
                                   /_/

"""
from enum_properties.meta import (
    EnumProperties,
    EnumPropertiesMeta,
    SymmetricMixin,
    p,
    s,
)

VERSION = (1, 0, 1)

__title__ = 'Enum Properties'
__version__ = '.'.join(str(i) for i in VERSION)
__author__ = 'Brian Kohan'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Brian Kohan'
