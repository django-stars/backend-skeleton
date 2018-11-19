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

        def aux(t):
            if len(t) == 3:
                return t
            elif len(t) == 2:
                return t[0], t[1], t[1]
            else:
                assert False, 'Incorrect format for input data'

        def check_for_unique(t):
            indexes_count = len(set([i[0] for i in t]))
            assert indexes_count == len(t)
            if len(t) > 2:
                human_readable_indexes_count = len(set([i[1] for i in t]))
                assert human_readable_indexes_count == len(t)

        check_for_unique(enum_list)
        self._full_enum_list = tuple(enum_list)
        enum_list = [aux(i) for i in enum_list]
        self._enum_list = [(item[0], item[2]) for item in enum_list]
        self._enum_dict = {}
        for item in enum_list:
            self._enum_dict[item[1]] = (item[0], item[2])

    def __add__(self, other):
        assert isinstance(other, Enumeration)
        new_enum_list = self._full_enum_list + other._full_enum_list
        return Enumeration(new_enum_list)

    def __contains__(self, v):
        return v in self.keys_list

    def __eq__(self, other):
        assert isinstance(other, Enumeration)
        return self._full_enum_list == other._full_enum_list

    def __getattr__(self, name):
        return self._enum_dict[name][0]

    def __getitem__(self, v):
        if isinstance(v, str):
            return self._enum_dict[v][0]
        elif isinstance(v, int):
            return self._enum_list[v]

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
        keys = [k for k in self.keys_list if k not in args]
        return Enumeration([t for t in self._full_enum_list if t[0] in keys])

    def get_name_by_value(self, v):
        return self.as_dict[v]

    @property
    def keys_list(self) -> list:
        return [el[0] for el in self._enum_list]
