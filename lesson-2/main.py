import os
import sys
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv


API_URL_TEMPLATE = 'https://api-ssl.bitly.com/v4/{}'


def shorten_link(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {
        'long_url': link
    }

    url = API_URL_TEMPLATE.format('shorten')

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    parsed = urlparse(link)
    summary_link = parsed.netloc + parsed.path

    # https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary
    url = API_URL_TEMPLATE.format(f'bitlinks/{summary_link}/clicks/summary')

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, link):
    parsed = urlparse(link)
    summary_link = parsed.netloc + parsed.path

    headers = {
        'Authorization': f'Bearer {token}'
    }

    # https://api-ssl.bitly.com/v4/bitlinks/{bitlink}
    query_url = API_URL_TEMPLATE.format(f'bitlinks/{summary_link}')
    response = requests.get(query_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_DVMN_TOKEN']
    user_link = input('Введите ссылку для подсчёта кликов или укорачивания: ')
    if is_bitlink(token, user_link):
        print('Ссылка', user_link, 'определена как битлинк')
        try:
            clicks_count = count_clicks(token, user_link)
        except requests.exceptions.HTTPError:
            print('Произошла ошибка. Проверьте верность введёных данных')
            sys.exit(1)
        print('На ссылку кликнули', clicks_count, 'раз(а)')
    else:
        print('Ссылка', user_link, 'определена как обычная')
        try:
            bitlink = shorten_link(token, user_link)
        except requests.exceptions.HTTPError:
            print('Произошла ошибка. Проверьте верность введёных данных')
            sys.exit(1)
        print('Укороченная ссылка:', bitlink)


if __name__ == '__main__':
    main()
