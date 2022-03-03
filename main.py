import requests
from vk import VKPhotoBackup
from ya import YaUploader
from logger import log

VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class ErrorChecker:

    def __init__(self, username, ya_token, album, photo_quantity, folder_name):
        self.username = username
        self.ya_token = ya_token
        self.album = album
        self.photo_quantity = photo_quantity
        self.folder_name = folder_name

    def token_validation(self):
        response = requests.get('https://cloud-api.yandex.net/v1/disk',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'OAuth {self.ya_token}'
                                })
        if response.status_code == 200:
            return True

    def is_number(self):
        try:
            int(self.photo_quantity)
            return True
        except ValueError:
            return False

    def check_folder(self):
        params = {
            'path': '/'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
        files = []
        for i in response.json()['_embedded']['items']:
            files.append(i['name'])
        if self.folder_name in files:
            return True
        else:
            return False

    def data_validation(self):
        log.info('starting data validation')
        log.info('cheking user existing')
        if not VKPhotoBackup(self.username, VK_TOKEN).get_user_id():
            log.error('user don`t exist')
            return
        log.info('checking account privacy')
        if not VKPhotoBackup(self.username, VK_TOKEN).all_photo_from_album():
            log.error('user`s profile is private')
            return
        log.info('checking yandex token')
        if not self.token_validation():
            log.error('not authorized')
            return
        log.info('checking album id')
        if not VKPhotoBackup(self.username, VK_TOKEN).all_photo_from_album(self.album):
            log.error('album error')
            return
        log.info('checking quantity')
        if not self.is_number():
            log.error('quantity error')
            return
        log.info('checking folder')
        if self.check_folder():
            log.error('folder already exist')
            return
        log.info('validation was successful')
        return True


if __name__ == '__main__':
    log.info("start program")
    username = 'begemot_korovin'
    ya_token = 'put your yandex token here'
    album_id = 'profile'
    photo_quantity = 2
    folder_name = 'Folder name'
    if ErrorChecker(username, ya_token, album_id, photo_quantity, folder_name).data_validation():
        log.info('creating new folder')
        YaUploader(ya_token, VKPhotoBackup(username, VK_TOKEN).get_user_id(), folder_name).create_folder()
        YaUploader(ya_token, VKPhotoBackup(username, VK_TOKEN).get_user_id(),
                   folder_name).upload_vkphoto(album_id=album_id, photo_quantity=photo_quantity)
    log.info('end program')

