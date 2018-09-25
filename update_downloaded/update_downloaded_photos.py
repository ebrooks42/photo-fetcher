from typing import List

import app_secrets
from models.PhotoLink import PhotoLink, to_photo_link
from update_downloaded.downloaded_photo_utils import delete_removed_photos_from_downloads, \
    add_new_photos_to_downloads, \
    get_downloaded_photo_ids
import photos_api


def update_downloaded_photos(access_token: str):
    updated_photo_links = get_photo_links(access_token)
    downloaded_photo_ids = get_downloaded_photo_ids()

    delete_removed_photos_from_downloads(downloaded_photo_ids, updated_photo_links)
    add_new_photos_to_downloads(access_token, downloaded_photo_ids, updated_photo_links)


def get_photo_links(access_token: str) -> List[PhotoLink]:
    def is_jpeg(media_item):
        return media_item['mimeType'] == 'image/jpeg'

    media_items = photos_api.get_media_items_for_album(access_token, app_secrets.ALBUM_ID)
    return [
        to_photo_link(item)
        for item in media_items
        if is_jpeg(item)
    ]
