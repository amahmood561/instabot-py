import datetime

import requests
import config
import json
def postInstagramQuote():
    #Post the Image
    image_location_1 = 'http:path-to-your-image.com/img/image-name.jpg'
    post_url = 'https://graph.facebook.com/v10.0/{}/media'.format(config.ig_user_id)
    payload = {
        'image_url': image_location_1,
        'caption': 'Get jobs online on https://careers-portal.co.za #career #hiring #jobs #job #jobssouthafrica #hiringnow',
        'access_token': config.user_access_token
        }
    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result:
        creation_id = result['id']
        second_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format(config.ig_user_id)
        second_payload = {
        'creation_id': creation_id,
        'access_token': config.user_access_token
        }
        r = requests.post(second_url, data=second_payload)
        print('--------Just posted to instagram--------')
        print(r.text)
    else:
        print('HOUSTON we have a problem')
postInstagramQuote()


def upload_post(self, image_path, caption=''):
    micro_time = int(datetime.now().timestamp())

    headers = {
        "content-type": "image / jpg",
        "content-length": "1",
        "X-Entity-Name": f"fb_uploader_{micro_time}",
        "Offset": "0",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "x-entity-length": "1",
        "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {micro_time}, "upload_media_height": 1080, "upload_media_width": 1080}}',
        "x-csrftoken": self.csrf_token,
        "x-ig-app-id": "1217981644879628",
        "cookie": self.cookie
    }

    upload_response = requests.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{micro_time}',
                                    data=open(image_path, "rb"), headers=headers, proxies=self.proxy)

    json_data = json.loads(upload_response.text)
    upload_id = json_data['upload_id']

    if json_data["status"] == "ok":
        url = "https://www.instagram.com/create/configure/"

        payload = 'upload_id=' + upload_id + '&caption=' + caption + '&usertags=&custom_accessibility_caption=&retry_timeout='
        headers = {
            'authority': 'www.instagram.com',
            'x-ig-www-claim': 'hmac.AR2-43UfYbG2ZZLxh-BQ8N0rqGa-hESkcmxat2RqMAXejXE3',
            'x-instagram-ajax': 'adb961e446b7-hot',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': self.csrf_token,
            'x-ig-app-id': '1217981644879628',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.instagram.com/create/details/',
            'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'cookie': self.cookie
        }

        response = requests.request("POST", url, headers=headers, data=payload, proxies=self.proxy)
        json_data = json.loads(response.text)

        if json_data["status"] == "ok":
            return 200

    else:
        return 400
