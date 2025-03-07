import sys
import pytest
import warnings


if sys.version_info < (3, 9):
    # because we import typing.Annotated for brevity in the examples
    # TODO remove after drop 3.8 support
    pytest.skip("requires Python 3.9 or higher", allow_module_level=True)


def test_basic_color_example():
    from tests.examples import color_example


def test_symmetric_example():
    from tests.examples import symmetric_example


def test_specialization_example():
    from tests.examples import specialization_example


def test_address_tutorial():
    from tests.examples import address


def test_mapbox_tutorial():
    from tests.examples import mapbox


def test_howto_add_props():
    from tests.examples import howto_add_props


def test_howto_metaclass():
    from tests.examples import howto_metaclass


def test_howto_symmetry():
    from tests.examples import howto_symmetry


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python 3.10 or higher")
def test_howto_symmetric_overload():
    from tests.examples import howto_symmetric_overload


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires Python 3.11 or higher")
def test_howto_verify_unique():
    with pytest.raises(ValueError):
        from tests.examples import howto_verify_unique


def test_howto_symmetric_builtins():
    from tests.examples import howto_symmetric_builtins


def test_howto_symmetric_decorator():
    from tests.examples import howto_symmetric_decorator


def test_howto_specialized():
    from tests.examples import howto_specialized


def test_howto_specialized_default():
    from tests.examples import howto_specialized_default


def test_howto_specialized_missing():
    from tests.examples import howto_specialized_missing


def test_howto_specialized_list():
    from tests.examples import howto_specialized_list


def test_howto_flag():
    from tests.examples import howto_flag


def test_howto_flag_no_iterable():
    with pytest.raises(AttributeError):
        from tests.examples import howto_flags_no_iterable


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires Python 3.11 or higher")
def test_howto_flag_boundaries():
    with pytest.raises(ValueError):
        from tests.examples import howto_flag_boundaries


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires Python 3.11 or higher")
def test_howto_nested_classes():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from tests.examples import howto_nested_classes_313


@pytest.mark.skipif(sys.version_info >= (3, 13), reason="requires Python < 3.13")
def test_howto_nested_classes_313():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from tests.examples import howto_nested_classes


def test_howto_dataclass():
    from tests.examples import howto_dataclass


def test_howto_dataclass_integration():
    from tests.examples import howto_dataclass_integration


def test_howto_hash_equiv():
    from tests.examples import howto_hash_equiv


def test_howto_hash_equiv_def():
    from tests.examples import howto_hash_equiv_def


def test_howto_legacy():
    from tests.examples import howto_legacy
