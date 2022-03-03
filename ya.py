import requests
import time
from logger import log
from vk import VKPhotoBackup
import json

VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class YaUploader:

    def __init__(self, ya_token, id_vk, folder_name):
        self.id_vk = id_vk
        self.ya_token = ya_token
        self.folder_name = folder_name
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }

    def create_folder(self):
        params = {
            'path': self.folder_name
        }
        response = requests.put(self.url, params=params, headers=self.headers)
        if response.status_code == 409:
            return False
        else:
            log.info('Folder create successfully')
            return self.folder_name

    def upload_vkphoto(self, album_id='profile', photo_quantity=5):
        log.info('start uploading photo')
        data = []
        for index, photo in enumerate(VKPhotoBackup(self.id_vk, VK_TOKEN).photo_with_best_quality(album_id).values()):
            if index not in range(photo_quantity):
                break
            else:
                temp_dict = {'file_name': f"{photo['file_name']}", 'size': photo['size']}
                data.append(temp_dict)
                params = {
                    'url': photo['url'],
                    'path': f'/{self.folder_name}/{photo["file_name"]}'
                }
                time.sleep(3)
                requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload/',
                              params=params, headers=self.headers)
                log.info(f'photo №{index + 1} upload successfully!')
        log.info('end uploading photo')
        log.info(f'now you can find your photo here: https://disk.yandex.ru/client/disk/{self.folder_name}')
        with open('file.json', 'w') as f:
            json.dump(data, f)
        log.info('saving data of backup')
        return

#
# YaUploader(YA_TOKEN, '1837308', '12').create_folder()
# YaUploader(YA_TOKEN, '1837308', '12').upload_vkphoto(album_id='173112353')
