import unittest

from pymalscraper.scraper import MALScraper
from pymalscraper.models import Anime


class AnimeScraperTest(unittest.TestCase):
    def setUp(self):
        self.scraper = MALScraper()

    def test_search_anime_kimi_no_na_wa(self):
        results = self.scraper.search_anime('kimi no na wa')

        for result in results:
            self.assertTrue(type(result), Anime)

    def test_anime_search_errors(self):
        with self.assertRaises(ValueError):
            self.scraper.search_anime('re')

        with self.assertRaises(TypeError):
            self.scraper.search_anime(101)

    def test_get_anime_list_from_60_to_90(self):
        anime_list = self.scraper.get_anime_list(60, 90)
        self.assertEqual(30, len(anime_list))

    def test_anime_list_contains_anime_objects(self):
        anime_list = self.scraper.get_anime_list(0, 20)

        for anime in anime_list:
            self.assertEqual(Anime, type(anime))


class CharacterScraperTest(unittest.TestCase):

    def setUp(self):
        self.scraper = MALScraper()
