from typing import List, Iterable
import pprint
import grequests

import utils
from models.Photo import Photo
from models.PhotoLink import PhotoLink
from models.MediaSearchResults import MediaSearchResults


def get_media_items_for_album(access_token, album_id) -> List:
    """
    Gets a list of media items in album with id album_id with access_token. Returns a list of
    Google Photos API media items.
    """
    search_data = {'albumId': album_id, 'pageSize': 100}

    media_items = []
    for result in MediaSearchResults(access_token, search_data):
        media_items += result['mediaItems']

    return media_items


def get_photos(access_token: str, photo_links: List[PhotoLink]) -> List[Photo]:
    """
    Gets photos referenced in photo_links with access_token. Returns List[Photo].
    """
    print(f'Fetching {len(photo_links)} photos.')
    photo_requests = get_photo_requests(access_token, photo_links)

    responses = get_photo_responses(photo_requests)

    images_as_bytes = [response.content for response in responses]
    photo_ids = [photo.id for photo in photo_links]

    return [
        Photo(id=id, bytes=bytes)
        for id, bytes in zip(photo_ids, images_as_bytes)
    ]


def get_photo_requests(access_token: str, photo_links: List[PhotoLink]) -> \
        List[grequests.AsyncRequest]:
    return [
        grequests.get(photo_link.url, params={'access_token': access_token})
        for photo_link in photo_links
    ]


def get_photo_responses(photo_requests: List[grequests.AsyncRequest]):
    request_chunks = utils.chunk(photo_requests, 10)
    num_chunks = len(request_chunks)

    responses = []
    for i, request_chunk in enumerate(request_chunks):
        print(f'Fetching photos in chunk {i + 1} of {num_chunks} chunks.')
        responses += get_response_chunk(request_chunk)

    return responses


def get_response_chunk(request_chunk: Iterable[grequests.AsyncRequest]):
    def handle_failed(response, exception):
        print(f'Request for photo failed for photo at URL:\n\t\t{response.url}')
        print("Details:")
        pprint.pprint(exception, width=1)

        return response

    return grequests.map(request_chunk, exception_handler=handle_failed)


def is_successful(response):
    return not response.exception
