# Anime Web Scraper

Scrapes data from https://myanimelist.net/.

## Anime Model

| Data           |   Attribute    | Description                                            |
| -------------- | :------------: | ------------------------------------------------------ |
| Title          |     title      | Main title in english characters.                      |
| English Title  | english_title  | English translation of the main title.                 |
| Japanese Title | japanese_title | Main title in japanese characters.                     |
| Synonyms       |    synonyms    | Other titles of the anime.                             |
| Synopsis       |    synopsis    | Synopsis / summary of the anime.                       |
| Anime Type     |   animetype    | Type of the anime.                                     |
| Episodes       |    episodes    | Number of episodes.                                    |
| Genres         |     genres     | Genres of the anime.                                   |
| Poster         |     poster     | Cover image of the anime.                              |
| Trailer        |    trailer     | Trailer of the anime.                                  |
| Data           |   get_data()   | Function that returns all of the data as a dictionary. |

## Character Model

| Data          |   Attribute   | Description                                                  |
| ------------- | :-----------: | ------------------------------------------------------------ |
| Name          |     name      | Name in english characters.                                  |
| Japanese Name | japanese_name | Name in japanese characters.                                 |
| Details       |    details    | About the character.                                         |
| Poster        |    poster     | Image of the character.                                      |
| Gallery       | get_gallery() | Function that scrapes the all the pictures of the character. |

## Installation

```
pip install pymalscraper
```

## Basic Usage

```python
from pymalscraper.scraper import MALScraper
scraper = MALScraper()
```

**Scraping Anime**

```python
results = scraper.search_anime("kimi no na wa.")
```

Will return a list of `Anime` instances

```
[ models.Anime<Kimi no Na wa.>,
models.Anime<Suntory Minami Alps no Tennensui>,
models.Anime<Kimi ni Todoke>,
models.Anime<Kimi ni Todoke 2nd Season>,
models.Anime<Kimi to Boku. 2> ]
```

**Scraping Character**

```python
results = scraper.search_character("mitsuha")
```

Will return a list of `Character` objects

```
[ models.Anime<Mitsuha>,
models.Anime<Mitsuha Miyamizu>,
models.Anime<Mitsuharu Moriya>,
models.Anime<Mother Mitsuhashi>,
models.Anime<Akari Mitsuhashi> ]
```

**To know more about the objects / instances, refer to the model section above.**

There is also a method in the scraper that scrapes the top list of either anime / characters.

```python
anime_list = scraper.get_anime_list(0, 50)
character_list = scraper.get_character_list(0, 50)
```

You just need to specify where to start (1st arg) and end (2nd arg) in the list.
