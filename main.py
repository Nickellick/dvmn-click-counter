import argparse
import os
import requests
import sys

from dotenv import load_dotenv
from urllib.parse import urlparse


def init_argparse():
    parser = argparse.ArgumentParser(
        description='bit.ly link shortener / click counter'
    )
    parser.add_argument(
        'link',
        help='Link to shrink/count'
    )
    return parser.parse_args()


def shorten_link(token, link_to_shorten):
    api_url = 'https://api-ssl.bitly.com/v4/shorten'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'long_url': link_to_shorten
    }

    response = requests.post(api_url, headers=headers, json=payload)
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
    args = init_argparse()
    token = os.environ['BITLY_DVMN_TOKEN']
    user_link = args.link
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
