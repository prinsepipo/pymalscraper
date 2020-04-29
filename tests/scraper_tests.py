import unittest

from pymalscraper.scraper import MALScraper
from pymalscraper.models import Anime, Character


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

    def test_mitsuha_search_results_length_is_5(self):
        results = self.scraper.search_character('mitsuha')
        self.assertEqual(len(results), 5)

    def test_character_mitsuha_search_results_are_character_objects(self):
        results = self.scraper.search_character('mitsuha')

        for result in results:
            self.assertIsInstance(result, Character)

    def test_search_with_less_than_3_letters_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.scraper.search_character('m')

        with self.assertRaises(ValueError):
            self.scraper.search_character('mi')

    def test_search_with_non_string_value_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.scraper.search_character(9)

        with self.assertRaises(TypeError):
            self.scraper.search_character(["mitsuha"])

        with self.assertRaises(TypeError):
            self.scraper.search_character(('mitsuha', ))

    def test_get_character_list_from_20_to_30(self):
        character_list = self.scraper.get_character_list(20, 30)
        self.assertEqual(len(character_list), 10)

    def test_get_character_list_contains_character_objects(self):
        character_list = self.scraper.get_character_list(0, 20)

        for character in character_list:
            self.assertIsInstance(character, Character)
