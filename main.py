import os
import requests
import sys

from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, link_to_shorten):
    api_url_template = 'https://api-ssl.bitly.com/v4/{}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'long_url': link_to_shorten
    }

    url = api_url_template.format('shorten')

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, link):
    api_url_template = 'https://api-ssl.bitly.com/v4/{}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    parsed_link = urlparse(link)
    summary_link = f'{parsed_link.netloc}{parsed_link.path}'

    url = api_url_template.format(f'bitlinks/{summary_link}/clicks/summary')

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, link):
    api_url_template = 'https://api-ssl.bitly.com/v4/{}'
    parsed_link = urlparse(link)
    summary_link = f'{parsed_link.netloc}{parsed_link.path}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = api_url_template.format(f'bitlinks/{summary_link}')
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_DVMN_TOKEN']
    user_link = input('Введите ссылку для подсчёта кликов или укорачивания: ')
    try:
        if is_bitlink(token, user_link):
            print(f'Ссылка {user_link} определена как битлинк')
            clicks_amount = count_clicks(token, user_link)
            print(f'На ссылку кликнули {clicks_amount} раз(а)')
        else:
            print(f'Ссылка {user_link} определена как обычная')
            short_link = shorten_link(token, user_link)
            print(f'Укороченная ссылка: {short_link}')
    except requests.exceptions.HTTPError:
        print('Произошла ошибка. Проверьте верность введёных данных')
        sys.exit(1)


if __name__ == '__main__':
    main()
