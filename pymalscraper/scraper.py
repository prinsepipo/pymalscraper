from .models import Anime, Character
from .shortcuts import get

import requests
from bs4 import BeautifulSoup

import time
from concurrent.futures import ThreadPoolExecutor


class Scraper:
    """
    Scrape data from https://myanimelist.net/.
    """

    def __init__(self):
        """
        Initialize the scraper.
        """
        # MAL search url
        self.MAL_ANIME_URL = 'https://myanimelist.net/anime.php?q='
        self.MAL_CHAR_URL = 'https://myanimelist.net/character.php?q='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }

    def search_anime(self, name):
        """
        Args:
            name: Name of anime.

        Returns:
            Return a list of tuple that contains the nane and url of the anime.
        """
        url = self.MAL_ANIME_URL + name
        res = get(url, self.headers)

        if res.status_code != 200:
            raise Exception(f'Response code {res.status_code}.')

        soup = BeautifulSoup(res.text, features='lxml')
        queryset = []

        try:
            div = soup.find(
                'div', {'class': 'js-categories-seasonal js-block-list list'})
            table_rows = div.find_all('tr')[1:5]

            for row in table_rows:
                td = row.find_all('td')[1]
                a = td.find('a')
                queryset.append((a.text, a['href']))
        except Exception as e:
            print(f'Parse Error\n.{e}')

        return queryset

    def get_anime(self, name=None, url=None):
        """
        Get the anime model data. Method only accepts one parameter, either name or url.

        Args:
            name: The name of the anime.
            url: The url of the anime.

        Returns:
            Return the Anime model data.
        """
        anime_url = None

        if name and not url:
            anime_url = self.search_anime(str(name))[0][1]
        elif url and not name:
            anime_url = url
        else:
            raise ValueError('Method needs one parameter, anime or url.')

        return Anime(anime_url)

    def get_all_anime(self, start=0, end=16150):
        """
        Scrape all the anime from the website. Scrapes 50 anime each method call.
        Note: Stoping the process will result to loss of data.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

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
            res = get(url, headers=self.headers)
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
        """
        # Gets the character url.
        char_url = self.get_character_url(str(name))

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
        res = get(url, headers=self.headers)
        soup = BeautifulSoup(res.text, features='lxml')
        lnk = None

        try:
            a = soup.find('div', {'id': 'content'})
            table = a.find('table',
                           {'width': '100%', 'cellspacing': '0', 'cellpadding': '0', 'border': '0'})
            td = table.find('td', {'width': '175'})
            a = td.find('a')
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
            res = get(url, headers=self.headers)
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
