import requests
import os
from datetime import datetime
import json
from bs4 import BeautifulSoup as bs
import time
import random
import string


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




class MyIGBot:
    def __init__(self, username, password, use_cookie=True, proxy=None):
        self.username = username
        self.password = password
        self.use_cookie = use_cookie
        self.proxy = proxy

        self.path = os.getcwd()

        if use_cookie == False or os.path.exists(self.path + f'//cookie_{self.username}.bot') == False:
            link = 'https://www.instagram.com/'
            login_url = 'https://www.instagram.com/accounts/login/ajax/'

            time_now = int(datetime.now().timestamp())
            response = requests.get(link, proxies=self.proxy)
            try:
                csrf = response.cookies['csrftoken']
            except:
                letters = string.ascii_lowercase
                csrf = ''.join(random.choice(letters) for i in range(8))

            payload = {
                'username': self.username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time_now}:{self.password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }

            login_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": csrf
            }

            login_response = requests.post(login_url, data=payload, headers=login_header, proxies=self.proxy)
            json_data = json.loads(login_response.text)

            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            try:
                self.csrf_token = cookie_jar['csrftoken']
            except:
                self.csrf_token = csrf

            try:
                if json_data["authenticated"]:
                    pass
                else:
                    print(bcolors.FAIL + "[✗] Login Failed!" + bcolors.ENDC, login_response.text)
                    quit()
            except KeyError:
                try:
                    if json_data["two_factor_required"]:
                        self.ig_nrcb = cookie_jar['ig_nrcb']
                        self.ig_did = cookie_jar['ig_did']
                        self.mid = cookie_jar['mid']

                        otp = input(bcolors.OKBLUE + '[!] Two Factor Auth. Detected! Enter Code Here: ' + bcolors.ENDC)
                        twofactor_url = 'https://www.instagram.com/accounts/login/ajax/two_factor/'
                        twofactor_payload = {
                            'username': self.username,
                            'verificationCode': otp,
                            'identifier': json_data["two_factor_info"]["two_factor_identifier"],
                            'queryParams': {}
                        }

                        twofactor_header = {
                            "accept": "*/*",
                            "accept-encoding": "gzip, deflate, br",
                            "accept-language": "en-US,en;q=0.9",
                            "content-type": "application/x-www-form-urlencoded",
                            "cookie": 'ig_did=' + self.ig_did + '; ig_nrcb=' + self.ig_nrcb + '; csrftoken=' + self.csrf_token + '; mid=' + self.mid,
                            "origin": "https://www.instagram.com",
                            "referer": "https://www.instagram.com/accounts/login/two_factor?next=%2F",
                            "sec-fetch-dest": "empty",
                            "sec-fetch-mode": "cors",
                            "sec-fetch-site": "same-origin",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                            "x-csrftoken": self.csrf_token,
                            "x-ig-app-id": "936619743392459",
                            "x-ig-www-claim": "0",
                            "x-instagram-ajax": "00c4537694a4",
                            "x-requested-with": "XMLHttpRequest"
                        }

                        login_response = requests.post(twofactor_url, data=twofactor_payload, headers=twofactor_header,
                                                       proxies=self.proxy)
                        try:
                            if login_response.headers['Set-Cookie'] != 0:
                                pass
                        except:
                            try:
                                if json_data["message"] == "checkpoint_required":
                                    self.ig_nrcb = cookie_jar['ig_nrcb']
                                    self.ig_did = cookie_jar['ig_did']
                                    self.mid = cookie_jar['mid']
                                    url = 'https://www.instagram.com' + json_data['checkpoint_url']
                                    header = {
                                        "accept": "*/*",
                                        "accept-encoding": "gzip, deflate, br",
                                        "accept-language": "en-US,en;q=0.9",
                                        "content-type": "application/x-www-form-urlencoded",
                                        "cookie": 'ig_did=' + self.ig_did + '; ig_nrcb=' + self.ig_nrcb + '; csrftoken=' + self.csrf_token + '; mid=' + self.mid,
                                        "origin": "https://www.instagram.com",
                                        "referer": 'https://instagram.com' + json_data['checkpoint_url'],
                                        "sec-fetch-dest": "empty",
                                        "sec-fetch-mode": "cors",
                                        "sec-fetch-site": "same-origin",
                                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                                        "x-csrftoken": self.csrf_token,
                                        "x-ig-app-id": "936619743392459",
                                        "x-ig-www-claim": "0",
                                        "x-instagram-ajax": "e8e20d8ba618",
                                        "x-requested-with": "XMLHttpRequest"
                                    }
                                    code = input(bcolors.OKBLUE + json.loads(
                                        requests.post(url, headers=header, data={'choice': '1'}).text,
                                        proxies=self.proxy)['extraData']['content'][1]['text'] + ' > ' + bcolors.ENDC)
                                    if json.loads(requests.post(url, headers=header, data={'security_code': code}).text,
                                                  proxies=self.proxy)['type'] == 'CHALLENGE_REDIRECTION':
                                        login_response = requests.post(login_url, data=payload, headers=login_header,
                                                                       proxies=self.proxy)
                                    else:
                                        print(bcolors.FAIL + '[✗] Login Failed!' + bcolors.ENDC)
                                        quit()
                            except:
                                print(bcolors.FAIL + '[✗] Login Failed!' + bcolors.ENDC)
                                quit()

                except KeyError:
                    try:
                        if json_data["message"] == "checkpoint_required":
                            self.ig_nrcb = cookie_jar['ig_nrcb']
                            self.ig_did = cookie_jar['ig_did']
                            self.mid = cookie_jar['mid']
                            url = 'https://www.instagram.com' + json_data['checkpoint_url']
                            header = {
                                "accept": "*/*",
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": "en-US,en;q=0.9",
                                "content-type": "application/x-www-form-urlencoded",
                                "cookie": 'ig_did=' + self.ig_did + '; ig_nrcb=' + self.ig_nrcb + '; csrftoken=' + self.csrf_token + '; mid=' + self.mid,
                                "origin": "https://www.instagram.com",
                                "referer": 'https://instagram.com' + json_data['checkpoint_url'],
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                                "x-csrftoken": self.csrf_token,
                                "x-ig-app-id": "936619743392459",
                                "x-ig-www-claim": "0",
                                "x-instagram-ajax": "e8e20d8ba618",
                                "x-requested-with": "XMLHttpRequest"
                            }
                            code = input(bcolors.OKBLUE +
                                         json.loads(requests.post(url, headers=header, data={'choice': '1'}).text,
                                                    proxies=self.proxy)['extraData']['content'][1][
                                             'text'] + ' > ' + bcolors.ENDC)
                            if json.loads(requests.post(url, headers=header, data={'security_code': code}).text,
                                          proxies=self.proxy)['type'] == 'CHALLENGE_REDIRECTION':
                                login_response = requests.post(login_url, data=payload, headers=login_header,
                                                               proxies=self.proxy)
                            else:
                                print(bcolors.FAIL + '[✗] Login Failed!' + bcolors.ENDC)
                                quit()
                    except:
                        print(bcolors.FAIL + '[✗] Login Failed!' + bcolors.ENDC)
                        quit()

            self.sessionid = login_response.headers['Set-Cookie'].split('sessionid=')[1].split(';')[0]
            self.userId = login_response.headers['Set-Cookie'].split('ds_user_id=')[1].split(';')[0]
            self.cookie = "sessionid=" + self.sessionid + "; csrftoken=" + self.csrf_token + "; ds_user_id=" + self.userId + ";"
            create_cookie = open(self.path + f'//cookie_{self.username}.bot', 'w+', encoding='utf-8')
            create_cookie.write(self.cookie)
            create_cookie.close()
            self.session = requests.session()
            cookie_obj = requests.cookies.create_cookie(
                name='sessionid', secure=True, value=self.sessionid)
            self.session.cookies.set_cookie(cookie_obj)

        elif os.path.exists(self.path + f'//cookie_{self.username}.bot'):
            try:
                read_cookie = open(self.path + f'//cookie_{self.username}.bot', 'r', encoding='utf-8')
                self.cookie = read_cookie.read()
                read_cookie.close()
                homelink = 'https://www.instagram.com/op/'
                self.session = requests.session()
                self.sessionid = self.cookie.split('=')[1].split(';')[0]
                self.csrf_token = self.cookie.split('=')[2].split(';')[0]
                cookie_obj = requests.cookies.create_cookie(
                    name='sessionid', secure=True, value=self.sessionid)
                self.session.cookies.set_cookie(cookie_obj)
                login_response = self.session.get(homelink, proxies=self.proxy)
                time.sleep(1)
                soup = bs(login_response.text, 'html.parser')
                soup.find("strong", {"class": "-cx-PRIVATE-NavBar__username -cx-PRIVATE-NavBar__username__"}).get_text()
            except AttributeError:
                print(bcolors.FAIL + "[✗] Login Failed! Cookie file is corupted!" + bcolors.ENDC)
                os.remove(self.path + f'//cookie_{self.username}.bot')
                print(bcolors.WARNING + "[-] Deleted Corupted Cookie File! Try Again!" + bcolors.ENDC)
                quit()
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
