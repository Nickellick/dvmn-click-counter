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

    headers = {
        'Authorization': f'Bearer {token}'
    }

    parsed_link = urlparse(link)

    api_url = 'https://api-ssl.bitly.com/v4/'\
        f'bitlinks/{parsed_link.netloc}{parsed_link.path}/clicks/summary'

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, link):
    parsed_link = urlparse(link)

    headers = {
        'Authorization': f'Bearer {token}'
    }

    api_url = 'https://api-ssl.bitly.com/v4/'\
        f'bitlinks/{parsed_link.netloc}{parsed_link.path}'

    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    args = init_argparse()
    token = os.environ['BITLY_DVMN_TOKEN']
    try:
        if is_bitlink(token, args.link):
            print(f'Ссылка {args.link} определена как битлинк')
            clicks_amount = count_clicks(token, args.link)
            print(f'На ссылку кликнули {clicks_amount} раз(а)')
        else:
            print(f'Ссылка {args.link} определена как обычная')
            short_link = shorten_link(token, args.link)
            print(f'Укороченная ссылка: {short_link}')
    except requests.exceptions.HTTPError:
        print('Произошла ошибка. Проверьте верность введёных данных')
        sys.exit(1)


if __name__ == '__main__':
    main()
