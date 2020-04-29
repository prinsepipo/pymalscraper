import sys

from bs4 import BeautifulSoup

from .models import Anime, Character
from .shortcuts import get, log, printd


class MALScraper:
    '''
    Create an instance to scrape data from https://myanimelist.net/.
    '''

    def __init__(self):
        # MAL URLS
        self.BASE_URL = 'https://myanimelist.net'
        self.ANIME_SEARCH_URL = self.BASE_URL + '/anime.php?q='
        self.CHARACTER_SEARCH_URL = self.BASE_URL + '/character.php?q='

    def search_anime(self, name):
        '''
        Search the anime.

        Note that MAL only accepts string input query with atleast 3 characters.

        Args:
            name: Name of anime.

        Returns:
            Return a list `Anime` objects.

        Raises:
            TypeError: Argument `name` must be string.
            ValueError: Argument `name` length must be >= 3.
        '''
        if type(name) != str:
            raise TypeError('Argument `name` type must be string.')
        if len(name) < 3:
            raise ValueError('Argument `name` must be 3 or more characters.')

        url = self.ANIME_SEARCH_URL + name
        urls = []

        print(f'Searching anime {name}...')

        # Find the anime in the search page of the website then parse the url
        # and the title of the first 5 results.
        try:
            res = get(url)
            soup = BeautifulSoup(res.text, features='lxml')

            div = soup.find('div', {'id': 'content'}).find(
                'div', {'class': 'js-categories-seasonal js-block-list list'})

            # First `tr` in the website is not part of the results.
            results = div.find('table').find_all('tr')[1:]

            for result in results:
                link = result.find('td').find('a')
                urls.append(link['href'])
        except Exception as e:
            msg = f'Function `search_anime` exception.\nURL: {url}\nEXCEPTION: {e}\n'
            log(msg)
            print(msg)

        return [Anime(url) for url in urls[:5]]

    def get_anime_list(self, start=0, end=10000):
        '''
        Scrape the top anime list in https://myanimelist.net/topanime.php.

        Args:
            start: Where to begin in the list.
                Value must not be greater than `end` value.

            end: Where to stop in the list.
                Value must not be lower than `start` value.

        Returns:
            A list of `Anime` objects.

        Raises:
            ValueError: Argument `start` must be within 0 to 10000 and less than `end` value.

            ValueError: Argument `end` must be within 0 to 10000 and greater than `start` value.
        '''
        # Constriants.
        if start < 0 or start >= 10000 or start > end:
            raise ValueError(
                'Argument `start` must be within 0 to 10000 and less than `end` value.')
        if end > 10000 or end <= 0 or end < start:
            raise ValueError(
                'Argument `end` must be within 0 to 10000 and greater than `start` value.')

        # This will contain the urls of the anime.
        urls = []

        # Since the website paginates by 50, we need to make sure that our
        # pagination values is a multiple of 50 (either 0, 50, 100, 150, ...).
        # `page_start` value should be less than `start` value and
        # `page_end` value should be greater than `end` value. This way we can
        # return the contents of the list from the specified start and end.
        if start % 50 == 0:
            page_start = start
        else:
            page_start = start - (start % 50)
        if end % 50 == 0:
            page_end = end
        else:
            page_end = (end + 50) - (end % 50)

        while page_start <= page_end:
            url = self.BASE_URL + '/topanime.php?limit=' + str(page_start)

            try:
                res = get(url)
                soup = BeautifulSoup(res.text, features='lxml')

                div = soup.find('div', {'id': 'content'}).find(
                    'div', {'class': 'pb12'})
                rows = div.find(
                    'table', {'class': 'top-ranking-table'}).find_all('tr', {'class': 'ranking-list'})

                for row in rows:
                    a = row.find('div', {'class': 'detail'}).find(
                        'a', {'class': 'hoverinfo_trigger fl-l fs14 fw-b'})
                    urls.append(a['href'])
            except Exception as e:
                msg = f'Function `get_all_anime` exception.\nURL: {url}\nEXCEPTION: {e}\n'
                log(msg)
                print(msg)

            page_start += 50

        # Parse the urls starting from `start` to `end`.
        return list(map(Anime, urls[start: end]))

    def search_character(self, name):
        '''
        Search the character. Note that searches are not 100% accurate. To compensate,
        this returns 5 search results. Each result is a tuple containing the name then then url of the character.

        Args:
            name: Name of the character.

        Returns:
            Return a list of tuple containing name and url of the character.

        Raises:
            TypeError: Argument 'name' must be of type string.
            ValueError: Argument `name` must be 3 or more characters.
        '''
        if type(name) != str:
            raise TypeError('Argument `name` must be of type string.')
        elif len(name) < 3:
            raise ValueError('Argument `name` must be 3 or more characters.')

        url = self.CHARACTER_SEARCH_URL + name
        urls = []

        print(f'Searching character {name}...')

        try:
            res = get(url)
            soup = BeautifulSoup(res.text, features='lxml')

            content_div = soup.find('div', {'id': 'content'})
            results = content_div.find('table').find_all('tr')

            for result in results:
                link = result.find('a')
                urls.append(link['href'])
        except Exception as e:
            msg = f'Function `search_anime` exception.\nURL: {url}\nEXCEPTION: {e}\n'
            log(msg)
            print(msg)

        return list(map(Character, urls[:5]))

    def get_character_list(self, start=0, end=10000):
        '''
        Scrape all the anime from the website. Scrapes 50 anime from start to
        end.
        Note: Stopping the process will result to loss of data.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

        Returns:
            Return a list of Anime model data.

        Raises:
            ValueError: Argument `start` must be less than the`end` value.
            ValueError: Argument `end` must be greater than the `start` value
        '''
        # Constriants.
        if start < 0 or start >= 10000 or start > end:
            raise ValueError(
                'Argument `start` must be less than the `end` value.')
        if end > 10000 or end <= 0 or end < start:
            raise ValueError(
                'Argument `end` must be greater than the `start` value.')

        # Since the website paginates by 50, we need to make sure that our
        # pagination values is a multiple of 50 (either 0, 50, 100, 150, ...).
        # `page_start` value should be less than `start` value and
        # `page_end` value should be greater than `end` value. This way we can
        # return the contents of the list from the specified start and end.
        if start % 50 == 0:
            page_start = start
        else:
            page_start = start - (start % 50)
        if end % 50 == 0:
            page_end = end
        else:
            page_end = (end + 50) - (end % 50)

        # Get the url of the all the anime in each page visit.
        urls = []

        while page_start <= page_end:
            url = self.BASE_URL + '/character.php?limit=' + str(page_start)
            res = get(url)

            # Parse the response data.
            soup = BeautifulSoup(res.text, features='lxml')

            try:
                table = soup.find('div', {'id': 'content'}).find(
                    'table', {'class': 'characters-favorites-ranking-table'})
                table_rows = table.find_all('tr', {'class': 'ranking-list'})

                for row in table_rows:
                    a = row.find('td', {'class': 'people'}).find(
                        'div', {'class': 'information di-ib mt24'}).find('a')
                    urls.append(a['href'])
            except Exception as e:
                msg = f'Function `get_all_characters` exception.\nURL: {url}\nEXCEPTION: {e}\n'
                log(msg)
                print(msg)

            page_start += 50

        return list(map(Character, urls[start:end]))
