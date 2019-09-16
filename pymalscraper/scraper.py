from .models import Anime, Character

import requests
from bs4 import BeautifulSoup

import time
from concurrent.futures import ThreadPoolExecutor


class MALScraper:
    """
    Scrape https://myanimelist.net/.

    Methods:
        get_anime(anime), get_anime_url(anime)
    """

    def __init__(self):
        """
        Initialize the settings of the scraper.
        """
        # MAL search url
        self.MAL_ANIME_URL = 'https://myanimelist.net/anime.php?q='
        self.MAL_CHAR_URL = 'https://myanimelist.net/character.php?q='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }

    def get_anime(self, anime):
        """
        Get the anime model data.

        Args:
            anime: The name of the anime.

        Returns:
            Return the Anime model data.

        Raises:
            TypeError: Argument anime must be string.
        """
        if type(anime) != str:
            raise TypeError('Argument anime must be string.')

        # Gets the anime url.
        anime_url = self.get_anime_url(anime)

        return Anime(anime_url)

    def get_anime_url(self, anime):
        """Gets the url of the anime from the website.

        Args:
            anime: Name of the anime.

        Returns:
            Return the scraped anime url.
        """
        url = self.MAL_ANIME_URL + anime

        res = requests.get(url, headers=self.headers)
        req_count = 0
        while res.status_code != 200 and req_count <= 10:
            print(res.status_code)
            time.sleep(1)
            res = requests.get(url, headers=self.headers)
            req_count += 1

        soup = BeautifulSoup(res.text, features='lxml')
        lnk = None
        try:
            a = soup.find('a', {'class': 'hoverinfo_trigger fw-b fl-l'})
            lnk = a['href']
        except Exception as e:
            print(f'Error getting anime url.\nError: {e}')
        return lnk

    def get_all_anime(self, start=0, end=16150):
        """
        Scrape all the anime from the website. Scrapes 50 anime each method call.

        Args:
            start: Where to begin scraping.
            to: Where to end scraping.

        Returns:
            Return a list of Anime model data.

        Raises:
            ValueError: Argument start must be greater than or equal to 0, or less than or equal to 16150.
            ValueError: Argument end must be divisible by 50, or less than or equal to 16100.
        """
        if start < 0 or start > 16150:
            raise ValueError(
                'Argument start must be greater than or equal to 0, or less than or equal to 16150.')
        if end % 50 != 0 or end > 16150:
            raise ValueError(
                'Argument end must be divisible by 50, or less than or equal to 16100.')

        total_anime = end - 50
        count = start
        links = []

        while count <= total_anime:
            url = f'https://myanimelist.net/topanime.php?limit={count}'
            print(f'Parsing {url} ...')
            res = requests.get(url, headers=self.headers)

            while res.status_code != 200:
                print(res.status_code)
                time.sleep(1)
                res = requests.get(url, headers=self.headers)

            soup = BeautifulSoup(res.text, features='lxml')

            try:
                aa = soup.find_all(
                    'a', {'class': 'hoverinfo_trigger fl-l fs14 fw-b'})

                for a in aa:
                    link = a['href']

                    if link:
                        links.append(link)
            except Exception as e:
                print(e)

            count += 50

        print(f'Scraping animes total of {len(links)}')

        with ThreadPoolExecutor() as executor:
            animes = executor.map(Anime, links)

        return list(animes)

    def get_character(self, name):
        """
        Gets the character model data.

        Args:
            name: Name of the character.

        Returns:
            Return the Character model data.

        Raises:
            TypeError: Argument name must be string.
        """
        if type(name) != str:
            raise TypeError('Argument name must be string.')

        # Gets the character url.
        char_url = self.get_character_url(name)

        if char_url is None:
            print(f'{name} not found.')
            return None

        return Character(char_url)

    def get_character_url(self, name):
        """
        Gets the url of the character from the website.

        Args:
            name: Name of the character.

        Returns:
            Returns the scraped character url.
        """
        url = self.MAL_CHAR_URL + str(name)

        res = requests.get(url, headers=self.headers)
        req_count = 0
        while res.status_code != 200 and req_count <= 10:
            print(res.status_code)
            time.sleep(1)
            res = requests.get(url, headers=self.headers)
            req_count += 1

        soup = BeautifulSoup(res.text, features='lxml')
        lnk = None

        try:
            a = soup.find('div', {'id': 'content'}).find('table', {
                'width': '100%', 'cellspacing': '0', 'cellpadding': '0', 'border': '0'}).find('td', {'width': '175'}).find('a')
            lnk = a['href']
        except Exception as e:
            print(f'Error getting character url.\nError: {e}')

        return lnk

    def get_all_characters(self, start=0, end=10000):
        """
        Scrape all the character from the website. Scrapes 50 character each method call.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

        Returns:
            Return a list of Character model data.

        Raises:
            ValueError: Argument start must be greater than or equal to 0, or less than or equal to 16150.
            ValueError: Argument end must be divisible by 50, or less than or equal to 16100.
        """
        if start < 0 or start > 10000:
            raise ValueError(
                'Argument start must be greater than or equal to 0, or less than or equal to 16150.')
        if end % 50 != 0 or end > 10000:
            raise ValueError(
                'Argument end must be divisible by 50, or less than or equal to 16100.')

        total_anime = end - 50
        count = start
        links = []

        while count <= total_anime:
            url = f'https://myanimelist.net/character.php?limit={count}'
            print(f'Parsing {url} ...')

            res = requests.get(url, headers=self.headers)
            req_count = 0
            while res.status_code != 200 and req_count <= 10:
                time.sleep(1)
                res = requests.get(url, headers=self.headers)
                req_count += 1

            soup = BeautifulSoup(res.text, features='lxml')

            try:
                aa = soup.find('div', {'id': 'content'}).find_all(
                    'a', {'class': 'fs14 fw-b'})

                for a in aa:
                    link = a['href']

                    if link:
                        links.append(link)
            except Exception as e:
                print(e)

            count += 50

        with ThreadPoolExecutor() as executor:
            chars = executor.map(Character, links)

        return list(chars)
