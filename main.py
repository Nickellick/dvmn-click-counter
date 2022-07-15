import os
import requests
import sys

from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(api_url, token, link_to_shorten):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'long_url': link_to_shorten
    }

    url = api_url.format('shorten')

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(api_url, token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    parsed_link = urlparse(link)
    summary_link = f'{parsed_link.netloc}{parsed_link.path}'

    url = api_url.format(f'bitlinks/{summary_link}/clicks/summary')

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(api_url, token, link):
    parsed_link = urlparse(link)
    summary_link = f'{parsed_link.netloc}{parsed_link.path}'

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
        preambule_text = f'Ссылка {user_link} определена как битлинк'
        callable_function = count_clicks
        epilogue_template = 'На ссылку кликнули {} раз(а)'
    else:
        preambule_text = f'Ссылка {user_link} определена как обычная'
        callable_function = shorten_link
        epilogue_template = 'Укороченная ссылка: {}'
    print(preambule_text)
    try:
        callback_result = callable_function(api_url_template, token, user_link)
    except requests.exceptions.HTTPError:
        print('Произошла ошибка. Проверьте верность введёных данных')
        sys.exit(1)
    print(epilogue_template.format(callback_result))


if __name__ == '__main__':
    main()
