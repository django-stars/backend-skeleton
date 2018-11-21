class Enumeration:
    """
    Based on a snippet - http://djangosnippets.org/snippets/1647/

    A small helper class for more readable enumerations, and compatible
    with Django's choice convention. You may just pass the instance of
    this class as the choices argument of model/form fields.

    Example 1 - general usage:

    >>> STATUSES = Enumeration(
    >>>     [
    >>>         (100, 'NEW', 'New'),
    >>>         (200, 'PENDING', 'Pending'),
    >>>         (300, 'FINISHED', 'Finished'),
    >>>         (400, 'ARCHIVED', 'Archived'),
    >>>         (500, 'DELETED', 'Deleted'),
    >>>     ]
    >>> )
    >>> assert 100 in STATUSES
    >>> assert STATUSES.NEW in STATUSES
    >>> assert STATUSES.PENDING == 200
    >>> assert STATUSES[1] == (200, 'Pending')
    >>> assert STATUSES['PENDING'] == 200

    Example 2 - excluding elements:

    >>> WORKING_STATUSES = STATUSES.exclude(STATUSES.ARCHIVED, STATUSES.DELETED)
    >>> assert len(WORKING_STATUSES) == 3
    >>> assert STATUSES[0] == (100, 'New')
    >>> assert STATUSES[1] == (200, 'Pending')
    >>> assert STATUSES[2] == (300, 'Finished')

    Example 3 - adding new elements:

    >>> ERROR_STATUSES = Enumeration(
    >>>     [
    >>>         (910, 'ERROR_GENERAL', 'General error'),
    >>>         (920, 'ERROR_TECHNICAL', 'Technical error'),
    >>>         (930, 'ERROR_API_LIMIT', 'Error: API limit reached'),
    >>>     ]
    >>> )
    >>> ALL_STATUSES = STATUSES + ERROR_STATUSES
    >>> assert len(WORKING_STATUSES) == 8
    >>> assert STATUSES[0] == (100, 'New')
    >>> assert STATUSES[1] == (200, 'Pending')
    >>> assert STATUSES[2] == (300, 'Finished')
    >>> assert STATUSES[3] == (400, 'Archived')
    >>> assert STATUSES[4] == (500, 'Deleted')
    >>> assert STATUSES[5] == (910, 'General error')
    >>> assert STATUSES[6] == (920, 'Technical error')
    >>> assert STATUSES[7] == (930, 'Error: API limit reached')
    """

    def __init__(self, enum_list):

        def aux(item):
            if len(item) == 3:
                return item
            elif len(item) == 2:
                return item[0], item[1], item[1]
            else:
                assert False, 'Incorrect format for input data'

        def check_for_unique(items):
            indexes_count = len(set([item[0] for item in items]))
            assert indexes_count == len(items)
            if len(items) > 2:
                human_readable_indexes_count = len(set([item[1] for item in items]))
                assert human_readable_indexes_count == len(items)

        check_for_unique(enum_list)
        self._full_enum_list = tuple(enum_list)
        enum_list = [aux(item) for item in enum_list]
        self._enum_list = [(item[0], item[2]) for item in enum_list]
        self._enum_dict = {}
        for item in enum_list:
            self._enum_dict[item[1]] = (item[0], item[2])

    def __add__(self, other):
        if not isinstance(other, Enumeration):
            return NotImplemented
        return Enumeration(self._full_enum_list + other._full_enum_list)
    __radd__ = __add__
    __iadd__ = __add__

    def __contains__(self, value):
        return value in self.keys_list

    def __eq__(self, other):
        assert isinstance(other, Enumeration)
        return self._full_enum_list == other._full_enum_list

    def __getattr__(self, name):
        return self._enum_dict[name][0]

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._enum_dict[key][0]
        elif isinstance(key, int):
            return self._enum_list[key]

    def __iter__(self):
        return self._enum_list.__iter__()

    def __len__(self):
        return len(self._enum_list)

    @property
    def as_dict(self) -> dict:
        return dict(self._enum_list)

    @property
    def as_tuple(self) -> tuple:
        return tuple(self._enum_list)

    def exclude(self, *args):
        keys = [key for key in self.keys_list if key not in args]
        return Enumeration([item for item in self._full_enum_list if item[0] in keys])

    def get_name_by_value(self, value):
        return self.as_dict[value]

    @property
    def keys_list(self) -> list:
        return [item[0] for item in self._enum_list]
