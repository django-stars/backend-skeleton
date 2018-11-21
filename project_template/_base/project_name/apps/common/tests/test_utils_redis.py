import pytest

from {{ project_name }}.apps.common.utils.redis import redis_key


@pytest.mark.parametrize('func_args,func_kwargs,expected_result', [
    (('users', ), {}, 'users'),
    (('users', 'jane', 'foo', 'bar', ), {}, 'users:jane:foo:bar'),
    (('users', 'jane', 42, 'comments', ), {'delimiter': '#'}, 'users#jane#42#comments'),
])
def test_redis_key(func_args, func_kwargs, expected_result):
    assert redis_key(*func_args, **func_kwargs) == expected_result
