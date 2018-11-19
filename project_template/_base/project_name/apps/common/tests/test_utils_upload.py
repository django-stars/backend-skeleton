from unittest import mock

import pytest

from {{ project_name }}.apps.common.utils import handle_media_upload


@pytest.mark.parametrize('directory, generated_uuid, filename, expected_result', [
    (
        '',
        'a64c8d79-7a09-4161-85b2-2b9622105734',
        'file.jpg',
        '/a64c8d79-7a09-4161-85b2-2b9622105734/file.jpg',
    ),
    (
        '/path/to/directory',
        'a64c8d79-7a09-4161-85b2-2b9622105734',
        'file.jpg',
        '/path/to/directory/a64c8d79-7a09-4161-85b2-2b9622105734/file.jpg',
    ),
    (
        '/path/to/directory',
        'a64c8d79-7a09-4161-85b2-2b9622105734',
        'f',
        '/path/to/directory/a64c8d79-7a09-4161-85b2-2b9622105734/f',
    ),
])
@mock.patch('uuid.uuid4')
def test_handle_media_upload(mocked_uuid4, directory, generated_uuid, filename, expected_result):
    mocked_uuid4.return_value = generated_uuid

    assert handle_media_upload(directory, filename) == expected_result
