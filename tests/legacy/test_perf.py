import sys
from unittest import TestCase


class Unhashable:
    pass


class PerformanceAndMemoryChecks(TestCase):
    from tests.big_enum import ISOCountry

    def test_check_big_enum_size(self):
        """
        Memory benchmarks:

        v1.3.3 ISOCountry: 151966 bytes
        v1.4.0 ISOCountry: 105046 bytes
        """

        seen = {}
        total_size = 0
        for name, attr in vars(self.ISOCountry).items():
            total_size += sys.getsizeof(attr)
            seen[(id(attr))] = (name, sys.getsizeof(attr))

        for val in self.ISOCountry:
            for name, attr in vars(self.ISOCountry).items():
                if id(attr) not in seen:  # pragma: no cover
                    total_size += sys.getsizeof(attr)
                    seen[(id(attr))] = (name, sys.getsizeof(attr))

        print("Total Memory footprint of ISOCountry: {} bytes".format(total_size))

    def test_property_access_time(self):
        """
        Access benchmarks:

        v1.3.3 ISOCountry: ~1.05 seconds (macbook M1 Pro)
        v1.4.0 ISOCountry: ~0.196 seconds (macbook M1 Pro) (5.3x faster)
        """

        # use perf counter to time the length of a for loop execution
        from time import perf_counter

        for_loop_time = perf_counter()
        for i in range(1000000):
            self.ISOCountry.US.full_name

        for_loop_time = perf_counter() - for_loop_time
        print("for loop time: {}".format(for_loop_time))

    def test_symmetric_mapping(self):
        """
        Symmetric mapping benchmarks

        v1.4.0 ISOCountry: ~3 seconds (macbook M1 Pro)
        v1.4.1 ISOCountry: ~ seconds (macbook M1 Pro) (x faster)
        """
        self.assertEqual(
            self.ISOCountry(self.ISOCountry.US.full_name.lower()), self.ISOCountry.US
        )
        from time import perf_counter

        for_loop_time = perf_counter()
        for i in range(1000000):
            self.ISOCountry(self.ISOCountry.US.full_name.lower())

        for_loop_time = perf_counter() - for_loop_time
        print("for loop time: {}".format(for_loop_time))
