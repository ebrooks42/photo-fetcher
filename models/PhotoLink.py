import collections

PhotoLink = collections.namedtuple('PhotoLink', 'id url')


def to_photo_link(media_item) -> PhotoLink:
    # setting the width and height to 9999 pixels to make sure
    # we get full definition photos back
    full_definition_url = media_item['baseUrl'] + '=w9999-h9999'
    return PhotoLink(
        id=media_item['id'],
        url=full_definition_url,
    )
