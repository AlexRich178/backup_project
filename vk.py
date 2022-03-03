import requests


class VKPhotoBackup:

    def __init__(self, user_id, vk_token):
        self.user_id = user_id
        self.vk_token = vk_token
        self.url = 'https://api.vk.com/method/'

    def get_user_id(self):
        response = requests.get(f'{self.url}users.get',
                                params={
                                    'user_ids': self.user_id,
                                    'fields': 'screen_name',
                                    'access_token': self.vk_token,
                                    'v': '5.131'
                                })
        if not response.json()['response']:
            return False
        else:
            return response.json()['response'][0]['id']

    def available_albums(self):
        response = requests.get(f'{self.url}photos.getAlbums',
                                params={
                                    'owner_id': self.get_user_id(),
                                    'access_token': self.vk_token,
                                    'v': '5.131'
                                })
        albums = {
            'profile': 'profile',
            'wall': 'wall'
        }
        for album in response.json()['response']['items']:
            albums[album['title']] = album['id']
        return albums

    def all_photo_from_album(self, album_id='profile'):
        response = requests.get(f'{self.url}photos.get',
                                params={
                                    'owner_id': self.get_user_id(),
                                    'album_id': album_id,
                                    'extended': '1',
                                    'access_token': self.vk_token,
                                    'v': '5.131'
                                })
        if 'error' in response.json().keys():
            return False
        else:
            return response.json()

    def photo_with_best_quality(self, album_id='profile'):
        photo_quality_types = {
            's': 0,
            'm': 1,
            'x': 2,
            'o': 3,
            'p': 4,
            'q': 5,
            'r': 6,
            'y': 7,
            'z': 8,
            'w': 9
        }
        photo_with_best_quality = {}
        for photo in self.all_photo_from_album(album_id)['response']['items']:
            temp_dict = {'file_name': f"{photo['likes']['count']}.jpg"}
            photo_with_best_quality[photo['id']] = temp_dict
            new_quality_dict = {}
            for photo_size in photo['sizes']:
                new_quality_dict[photo_size['type']] = photo_quality_types.get(photo_size['type'])
                max_size = max(new_quality_dict, key=new_quality_dict.get)
                if photo_size['type'] == max_size:
                    temp_dict['size'] = photo_size['type']
                    temp_dict['url'] = photo_size['url']
        return photo_with_best_quality
