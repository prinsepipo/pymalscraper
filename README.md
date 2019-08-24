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
- Poster
- Trailer

## Installation
```
pip install pymalscraper
```

## Basic Usage
```python
from pymalscraper.scraper import MALScraper
scraper = MALScraper()
data = scraper.get_anime("kimi no na wa.")

> data.title
'Kimi no na wa.'
> data.english_title
'Your Name.'
> data.japanese_title
'君の名は。'
> data.synonyms
''
> data.synopsis
"Mitsuha Miyamizu, a high school girl, yearns to live the life of a boy in the bustling city of Tokyo—a dream that stands in stark contrast..."
> data.animetype
'Movie'
> data.episodes
'1'
> data.genres
'Romance, Supernatural, School, Drama'
> data.poster
'https://cdn.myanimelist.net/images/anime/5/87048.jpg'
> data.trailer
'https://www.youtube.com/embed/3KR8_igDs1Y?enablejsapi=1&wmode=opaque&autoplay=1'

# To get the anime url    
> scraper.get_anime_url('kimi no na wa.')
'https://myanimelist.net/anime/32281/Kimi_no_Na_wa'
```
