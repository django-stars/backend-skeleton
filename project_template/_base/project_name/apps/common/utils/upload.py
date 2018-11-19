import uuid


def handle_media_upload(directory, filename) -> str:  # pragma: no cover
    return '{directory}/{uid}/{filename}'.format(directory=directory, uid=uuid.uuid4(), filename=filename)
