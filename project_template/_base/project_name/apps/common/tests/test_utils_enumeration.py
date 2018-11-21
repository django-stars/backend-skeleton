import pytest

from {{ project_name }}.apps.common.utils.enumeration import Enumeration


def test_init():
    input_data = [
        (100, 'FOO', 'Foo'),
        (200, 'BAR', 'Bar'),
        (300, 'BAZ', 'Baz'),
    ]
    expected_enum_list = [
        (100, 'Foo'),
        (200, 'Bar'),
        (300, 'Baz'),
    ]
    expected_enum_dict ={
            'FOO': (100, 'Foo'),
            'BAR': (200, 'Bar'),
            'BAZ': (300, 'Baz'),
        }

    enumeration = Enumeration(input_data)

    assert isinstance(enumeration._full_enum_list, tuple)
    assert enumeration._full_enum_list == tuple(input_data)
    assert isinstance(enumeration._enum_list, list)
    assert enumeration._enum_list == expected_enum_list
    assert isinstance(enumeration._enum_dict, dict)
    assert enumeration._enum_dict == expected_enum_dict


def test_general_use():
    params = [
        (100, 'NEW', 'New'),
        (200, 'PENDING', 'Pending'),
        (300, 'FINISHED', 'Finished'),
        (400, 'ARCHIVED', 'Archived'),
        (500, 'DELETED', 'Deleted'),
    ]
    statuses = Enumeration(params)

    assert len(statuses) == 5

    for item_index, item in enumerate(params):
        int_value, str_key, caption = item
        assert hasattr(statuses, str_key)
        item = getattr(statuses, str_key)
        assert item == int_value  # assert STATUSES.NEW == 100
        assert int_value in statuses  # assert 100 in STATUSES
        assert item in statuses  # assert STATUSES.NEW in STATUSES
        assert statuses[item_index] == (int_value, caption)  # assert STATUSES[0] == (100, 'New')
        assert statuses[str_key] == int_value  # assert STATUSES['NEW'] == 100


def test_add():
    main_params = [
        (100, 'NEW', 'New'),
        (200, 'PENDING', 'Pending'),
        (300, 'FINISHED', 'Finished'),
        (400, 'ARCHIVED', 'Archived'),
        (500, 'DELETED', 'Deleted'),
    ]
    main_statuses = Enumeration(main_params)
    error_params = [
        (910, 'ERROR_GENERAL', 'General error'),
        (920, 'ERROR_TECHNICAL', 'Technical error'),
        (930, 'ERROR_API_LIMIT', 'Error: API limit reached'),
    ]
    error_statuses = Enumeration(error_params)
    all_params = main_params + error_params
    all_statuses = Enumeration(all_params)

    result = main_statuses + error_statuses

    assert result == all_statuses


def test_as_dict():
    params = [
        (100, 'FOO', 'Foo'),
        (200, 'BAR', 'Bar'),
        (300, 'BAZ', 'Baz'),
    ]
    statuses = Enumeration(params)

    statuses_dict = statuses.as_dict

    assert isinstance(statuses_dict, dict)
    assert statuses_dict == {
        100: 'Foo',
        200: 'Bar',
        300: 'Baz',
    }


def test_as_tuple():
    params = [
        (100, 'FOO', 'Foo'),
        (200, 'BAR', 'Bar'),
        (300, 'BAZ', 'Baz'),
    ]
    statuses = Enumeration(params)

    statuses_tuple = statuses.as_tuple

    assert isinstance(statuses_tuple, tuple)
    assert statuses_tuple == (
        (100, 'Foo'),
        (200, 'Bar'),
        (300, 'Baz'),
    )


def test_exclude():
    main_params = [
        (100, 'NEW', 'New'),
        (200, 'PENDING', 'Pending'),
        (300, 'FINISHED', 'Finished'),
        (400, 'ARCHIVED', 'Archived'),
        (500, 'DELETED', 'Deleted'),
    ]
    main_statuses = Enumeration(main_params)
    working_params = (
        (100, 'NEW', 'New'),
        (200, 'PENDING', 'Pending'),
        (300, 'FINISHED', 'Finished'),
    )
    working_statuses = Enumeration(working_params)

    result = main_statuses.exclude(main_statuses.ARCHIVED, main_statuses.DELETED)

    assert result == working_statuses


@pytest.mark.parametrize('value,name', [
    (100, 'Foo'),
    (200, 'Bar'),
    (300, 'Baz'),
    (42, None),
])
def test_get_name_by_value(value, name):
    params = [
        (100, 'FOO', 'Foo'),
        (200, 'BAR', 'Bar'),
        (300, 'BAZ', 'Baz'),
    ]
    statuses = Enumeration(params)

    if name is not None:
        assert statuses.get_name_by_value(value) == name
    else:
        with pytest.raises(KeyError):
            statuses.get_name_by_value(value)


def test_keys_list():
    params = [
        (100, 'FOO', 'Foo'),
        (200, 'BAR', 'Bar'),
        (300, 'BAZ', 'Baz'),
    ]
    statuses = Enumeration(params)

    assert statuses.keys_list == [100, 200, 300]
