import datetime
import sys
import time

import requests


def get(url):
    '''
    Custom get request. Recursively make request every designated interval.

    Args:
        url: URL link.

    Returns:
        Return the http response.
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }

    res = requests.get(url, headers=headers, timeout=(2, 5))
    max_request = 20

    if res.status_code != 200 and max_request != 0:
        res = get(url)
        max_request -= 1

    if max_request == 0:
        return None

    return res


def log(message):
    with open('pymalscraper.logs.txt', 'a') as f:
        logtime = str(datetime.datetime.now())
        f.write(f'----- {logtime} -----\n{message}\n\n')


def printd(string):
    '''Print dynamically.'''
    sys.stdout.write(f'\x1b[2K\r{string}')
    sys.stdout.flush()
