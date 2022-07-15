import os
import requests
import sys

from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(api_url, token, link_to_shorten):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {
        'long_url': link_to_shorten
    }

    url = api_url.format('shorten')

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(api_url, token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    parsed = urlparse(link)
    summary_link = f'{parsed.netloc}{parsed.path}'

    url = api_url.format(f'bitlinks/{summary_link}/clicks/summary')

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(api_url, token, link):
    parsed = urlparse(link)
    summary_link = f'{parsed.netloc}{parsed.path}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = api_url.format(f'bitlinks/{summary_link}')
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    api_url_template = 'https://api-ssl.bitly.com/v4/{}'
    token = os.environ['BITLY_DVMN_TOKEN']
    user_link = input('Введите ссылку для подсчёта кликов или укорачивания: ')
    if is_bitlink(api_url_template, token, user_link):
        print('Ссылка', user_link, 'определена как битлинк')
        try:
            clicks_count = count_clicks(api_url_template, token, user_link)
        except requests.exceptions.HTTPError:
            print('Произошла ошибка. Проверьте верность введёных данных')
            sys.exit(1)
        print('На ссылку кликнули', clicks_count, 'раз(а)')
    else:
        print('Ссылка', user_link, 'определена как обычная')
        try:
            bitlink = shorten_link(api_url_template, token, user_link)
        except requests.exceptions.HTTPError:
            print('Произошла ошибка. Проверьте верность введёных данных')
            sys.exit(1)
        print('Укороченная ссылка:', bitlink)


if __name__ == '__main__':
    main()
