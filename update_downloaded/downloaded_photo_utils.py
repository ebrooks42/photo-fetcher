from typing import List
import glob
import os

import utils
from constants import DOWNLOADED_PHOTOS_LOCATION
from models.PhotoLink import PhotoLink
from models.Photo import Photo
import photos_api


def get_downloaded_photo_ids() -> List[str]:
    return [
        get_photo_id(photo_path)
        for photo_path in glob.glob(f'{DOWNLOADED_PHOTOS_LOCATION}*.jpeg')
    ]


def add_new_photos_to_downloads(access_token: str,
                                downloaded_photo_ids: List[str],
                                updated_photo_links: List[PhotoLink]):
    current_photo_ids = [photo_link.id for photo_link in updated_photo_links]
    new_photo_ids = utils.diff(current_photo_ids, downloaded_photo_ids)

    if not new_photo_ids:
        return

    new_photo_links = [
        photo_link
        for photo_link in updated_photo_links
        if photo_link.id in new_photo_ids
    ]

    print("Adding new photos to downloaded folder.")
    print(f'{len(new_photo_ids)} out of {len(current_photo_ids)} photos need to be downloaded.')

    new_photos = photos_api.get_photos(access_token, new_photo_links)
    for photo in new_photos:
        add_photo_to_downloads(photo)


def delete_removed_photos_from_downloads(downloaded_photo_ids: List[str],
                                         updated_photo_links: List[PhotoLink]):
    current_photo_ids = [photo_link.id for photo_link in updated_photo_links]
    removed_photo_ids = utils.diff(downloaded_photo_ids, current_photo_ids)

    if not removed_photo_ids:
        return

    print("Removing old photos from downloaded folder.")
    print(f'{len(removed_photo_ids)} out of {len(current_photo_ids)} photos need to be deleted.')

    for removed_photo_id in removed_photo_ids:
        photo_path = to_downloaded_file_path(removed_photo_id)
        print(f'Deleting {photo_path}.')
        os.remove(photo_path)


def add_photo_to_downloads(photo: Photo):
    path = to_downloaded_file_path(photo.id)
    with open(path, 'wb') as photo_file:
        photo_file.write(photo.bytes)


def to_downloaded_file_path(photo_id: str) -> str:
    return f'{DOWNLOADED_PHOTOS_LOCATION}{photo_id}.jpeg'


def get_photo_id(photo_path: str) -> str:
    without_path = photo_path.replace(DOWNLOADED_PHOTOS_LOCATION, "")
    without_ext_and_path = without_path.replace(".jpeg", "")
    return without_ext_and_path
