import requests
import time
import json

us_id = input('input id: ')
vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
ya_disk_token = input('input token: ')
photo_count_def = 5


def download_files(use_id, token):
    user_id = use_id
    token = token
    url = 'https://api.vk.com/method/photos.get'
    params = {'user_ids': user_id, 'access_token': token, 'v': '5.131', 'album_id': 'profile', 'extended': '1'}
    res = requests.get(url, params=params)
    return res.json()['response']['items']


def sorting():
    data = download_files(us_id, vk_token)[0:photo_count_def - 1]
    print('Download completed')
    sorted_list = []

    for photo in data:
        sort_siz = []

        for size in photo['sizes']:
            sort_siz.append(int(size['height']) * int(size['width']))
        sort_siz.sort()

        for size in photo['sizes']:
            if int(size['height']) * int(size['width']) == sort_siz[-1]:
                sorted_list.append({'likes': photo['likes']['count'], 'url': size['url'], 'type': size['type']})

    return sorted_list


def worker():
    file_log = []
    filelist = sorting()
    folder_name = 'netology_photos'
    url1 = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Content-Type': 'application/json', 'Authorization': f"OAuth {ya_disk_token}"}
    params = {'path': folder_name, 'overwrite': 'true'}
    requests.put(url1, headers=headers, params=params)
    bar_num = (1 / int(len(filelist))) * 100
    bar = 0

    print('Uploading 0%')

    for file in filelist:
        time.sleep(0.30)
        params2 = {'path': f"{folder_name}/{file['likes']}_{file['type']}.jpg", 'overwrite': 'true'}
        url2 = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        link = requests.get(url2, headers=headers, params=params2)
        link_json = link.json()
        requests.put(link_json['href'], requests.get(file['url']).content)
        file_log.append({'file_name': f"{file['likes']}_{file['type']}.jpg", 'size': file['type']})
        bar += bar_num
        print(f"Uploading {round(bar)}%")

    with open('json_log.json', 'w') as f:
        json.dump(file_log, f)
    print('Done')


if __name__ == '__main__':
    worker()
