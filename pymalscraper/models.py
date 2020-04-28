from bs4 import BeautifulSoup
from bs4 import element

from .shortcuts import get, log


class Anime:
    def __init__(self, url):
        res = get(url)
        self._soup = BeautifulSoup(res.text, features='lxml')
        self.q = url.split('/')[-1]

        self.content_div = self._soup.find('div', {'id': 'content'})
        self.sidebar = self.content_div.find(
            'td', {'class': 'borderClass'}).find('div')

    @property
    def title(self):
        title = None

        try:
            div = self._soup.find('div', {'id': 'contentWrapper'})
            span = div.find('span', {'itemprop': 'name'})
            # This will give us just the inner text of the element without the
            # child elements, if there are.
            title = ''.join(
                [c for c in span.contents if type(c) == element.NavigableString])
        except Exception as e:
            print(f'{self.q} title: {e}')

        return title

    @property
    def english_title(self):
        title = None

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'English:' in div.text:
                    title = div.text.replace('English:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'{self.q} english title: {e}')

        return title

    @property
    def japanese_title(self):
        title = None

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'Japanese:' in div.text:
                    title = div.text.replace('Japanese:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'{self.q} japanese title: {e}')

        return title

    @property
    def synonyms(self):
        syn = None

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'Synonyms:' in div.text:
                    syn = div.text.replace(
                        'Synonyms:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'{self.q} synonyms: {e}')

        return syn

    @property
    def synopsis(self):
        synopsis = None

        try:
            span = self._soup.find('span', {'itemprop': 'description'})
            synopsis = span.text
        except Exception as e:
            print(f'{self.q} synopsis: {e}')

        return synopsis

    @property
    def animetype(self):
        anime_type = None

        try:

            divs = self.sidebar.find_all('div')

            for div in divs:
                if 'Type:' in div.text:
                    anime_type = div.find('a').text
                    break
        except Exception as e:
            print(f'{self.q} anime type: {e}')

        return anime_type

    @property
    def episodes(self):
        eps = None

        try:
            divs = self.sidebar.find_all('div')

            for div in divs:
                if 'Episodes:' in div.text:
                    eps = div.text.replace('Episodes:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'{self.q} episodes: {e}')

        return eps

    @property
    def genres(self):
        genres = None

        try:
            divs = self.sidebar.find_all('div')

            for div in divs:
                if 'Genres:' in div.text:
                    links = div.find_all('a')
                    genres = [a.text for a in links]
        except Exception as e:
            print(f'{self.q} genres: {e}')

        return genres

    @property
    def poster(self):
        poster = None

        try:
            img = self.sidebar.find('img')
            poster = img['data-src']
        except Exception as e:
            print(f'{self.q} poster: {e}')

        return poster

    @property
    def trailer(self):
        trailer = None

        try:
            a = self._soup.find(
                'a', {'class': 'iframe js-fancybox-video video-unit promotion'})
            trailer = a['href']
        except Exception as e:
            print(f'{self.q} trailer: {e}')

        return trailer

    def get_data(self):
        """
        Gets the full anime data in json.

        Returns:
            Dict object.
        """
        data = {
            'title': self.title,
            'english_title': self.english_title,
            'japanese_title': self.japanese_title,
            'synonyms': self.synonyms,
            'synopsis': self.synopsis,
            'type': self.animetype,
            'episodes': self.episodes,
            'genres': self.genres,
            'poster': self.poster,
            'trailer': self.trailer
        }

        return data

    def __repr__(self):
        return f'models.Anime<{self}>'

    def __str__(self):
        return self.title


class Character:
    def __init__(self, url):
        self._url = url
        self._soup = None
        self.q = url.split('/')[-1]

        try:
            res = get(url)
            self._soup = BeautifulSoup(res.text, features='lxml')
        except Exception as e:
            msg = f'Anime model exception.\nURL: {url}\nEXCEPTION: {e}\n'
            log(msg)
            print(msg)

    @property
    def name(self):
        name = None

        try:
            div = self._soup.find('div', {'id': 'content'}).find('table').find(
                'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find(
                'div', {'class': 'normal_header'})
            name = div.text

            if '(' in name:
                name = name[:name.find('(') - 1]

            name = name.rstrip()
        except Exception as e:
            print(f'{self.q} name: {e}')

        return name

    @property
    def japanese_name(self):
        name = None

        try:
            div = self._soup.find('div', {'id': 'content'}).find('table').find(
                'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find(
                'div', {'class': 'normal_header'})
            name = div.text

            if '(' in name:
                name = name[name.find('(') + 1:-1]

            name = name.rstrip()
        except Exception as e:
            print(f'{self.q} name: {e}')

        return name

    @property
    def alternate_names(self):
        name = None

        try:
            div = self._soup.find('div', {'id': 'contentWrapper'}).find('div')
            h1 = div.find('h1', {'class': 'h1'})
            name = h1.text

            if '"' in name:
                name = name.split('"', 2)[1]
        except Exception as e:
            print(f'{self.q} alternate_names: {e}')

        return name

    @property
    def details(self):
        details = None

        try:
            div = self._soup.find('div', {'id': 'content'}).find(
                'table').find('td',  {'style': 'padding-left: 5px;', 'valign': 'top'})
            details = div.text
            details = details[:details.find('Voice Actors')]
        except Exception as e:
            print(f'{self.q} details: {e}')

        return details

    @property
    def poster(self):
        poster = None

        try:
            img = self._soup.find('div', {'id': 'content'}).find('img')
            poster = img['src']
        except Exception as e:
            print(f'{self.q} poster: {e}')

        return poster

    def get_gallery(self):
        url = self._url + '/pictures'
        res = get(url)
        soup = BeautifulSoup(res.text, features='lxml')
        gallery = []

        try:
            imgs = soup.find('div', {'id': 'content'}).find(
                'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find(
                'table').find_all('img')

            for i, img in enumerate(imgs):
                try:
                    gallery.append(img['src'])
                except Exception as e:
                    print(e)
        except Exception as e:
            print(f'{self.q} gallery: {e}')

        return gallery

    def __repr__(self):
        return f'models.Anime<{self}>'

    def __str__(self):
        return self.name
