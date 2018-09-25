from requests import post
from constants import API_BASE_URL

SEARCH_URL = API_BASE_URL + '/mediaItems:search'


class MediaSearchResults:
    def __init__(self, access_token, search_data):
        self.access_token = access_token
        self.search_data = search_data

    def _search(self, page_token):
        params = {'access_token': self.access_token}
        data = self.search_data.copy()

        if page_token:
            data['pageToken'] = page_token

        return post(SEARCH_URL, params=params, data=data).json()

    def __iter__(self):
        page_token = ''
        while True:
            search_result = self._search(page_token)

            yield search_result

            # only keep searching if there is a next page available
            if search_result.get('nextPageToken', ''):
                page_token = search_result['nextPageToken']
            else:
                break
