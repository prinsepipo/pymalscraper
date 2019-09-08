# Anime Web Scraper
Scrapes anime data from https://myanimelist.net/ .

## Anime Model Data
These are, as for now, the only available data.
- Title
- English Title
- Japanese Title
- Synonyms
- Synopsis
- Anime Type
- Episodes
- Genres
- Poster (link)
- Trailer (link)

## Installation
```
pip install pymalscraper
```

## Basic Usage
```python
from pymalscraper.scraper import MALScraper
scraper = MALScraper()
anime = scraper.get_anime("kimi no na wa.")

> anime.title
'Kimi no na wa.'
> anime.english_title
'Your Name.'
> anime.japanese_title
'君の名は。'
> anime.synonyms
''
> anime.synopsis
"Mitsuha Miyamizu, a high school girl, yearns to live the life of a boy in the bustling city of Tokyo—a dream that stands in stark contrast to her present life in the countryside. Meanwhile in the city, Taki Tachibana lives a busy life as a high school student while juggling his part-time job and hopes for a future in architecture.\n\r\nOne day, Mitsuha awakens in a room that is not her own and suddenly finds herself living the dream life in Tokyo—but in Taki's body! Elsewhere, Taki finds himself living Mitsuha's life in the humble countryside. In pursuit of an answer to this strange phenomenon, they begin to search for one another.\n\nKimi no Na wa. revolves around Mitsuha and Taki's actions, which begin to have a dramatic impact on each other's lives, weaving them into a fabric held together by fate and circumstance.\n\r\n[Written by MAL Rewrite]"
> anime.animetype
'Movie'
> anime.episodes
'1'
> anime.genres
'Romance, Supernatural, School, Drama'
> anime.poster
'https://cdn.myanimelist.net/images/anime/5/87048.jpg'
> anime.trailer
'https://www.youtube.com/embed/3KR8_igDs1Y?enablejsapi=1&wmode=opaque&autoplay=1'

# To get the full data. By default, this returns json.
> anime.get_data()
{'title': 'Kimi no Na wa.', 'english_title': 'Your Name.', 'japanese_title': '君の名は。', 'synonyms': None, 'synopsis': "Mitsuha Miyamizu, a high school girl, yearns to live the life of a boy in the bustling city of Tokyo—a dream that stands in stark contrast to her present life in the countryside. Meanwhile in the city, Taki Tachibana lives a busy life as a high school student while juggling his part-time job and hopes for a future in architecture.\n\r\nOne day, Mitsuha awakens in a room that is not her own and suddenly finds herself living the dream life in Tokyo—but in Taki's body! Elsewhere, Taki finds himself living Mitsuha's life in the humble countryside. In pursuit of an answer to this strange phenomenon, they begin to search for one another.\n\nKimi no Na wa. revolves around Mitsuha and Taki's actions, which begin to have a dramatic impact on each other's lives, weaving them into a fabric held together by fate and circumstance.\n\r\n[Written by MAL Rewrite]", 'type': 'Movie', 'episodes': '1', 'genres': 'Romance, Supernatural, School, Drama', 'poster': 'https://cdn.myanimelist.net/images/anime/5/87048.jpg', 'trailer': 'https://www.youtube.com/embed/3KR8_igDs1Y?enablejsapi=1&wmode=opaque&autoplay=1'}

# To get the anime url    
> scraper.get_anime_url('kimi no na wa.')
'https://myanimelist.net/anime/32281/Kimi_no_Na_wa'
```
