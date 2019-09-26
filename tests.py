import unittest

from pymalscraper.scraper import Scraper
from pymalscraper.models import Anime


class AnimeTests(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    def test_get_anime(self):
        anime = self.scraper.get_anime('kimi no na wa')
        data = anime.get_data()
        self.assertEqual(type(data), type({}))

        # Data accepts anything except 'None'.
        for key in data.keys():
            value = data[key]
            self.assertIsNotNone(value)

            if value != '':
                if 'title' in key:
                    self.assertLessEqual(len(value), 100)
                elif 'synonyms' == key:
                    self.assertEqual(len(value), 300)
                elif 'type' == key:
                    self.assertIn(value.lower(), ['tv', 'movie'])
                elif 'episodes' == key:
                    self.assertLessEqual(len(value), 3)
                elif 'genres' == key:
                    self.assertLessEqual(len(value), 200)
                elif 'poster' == key or 'trailer' == key:
                    self.assertIn('http', value)
            else:
                self.assertTrue(value == '')

    def test_search_anime(self):
        results = self.scraper.search_anime('kimi no na wa')
        self.assertTrue(type(results) == type([]))
        self.assertLessEqual(len(results), 5)

    def test_get_all_anime(self):
        start = 0
        end = 50
        result = self.scraper.get_all_anime(start=0, end=50)

        self.assertTrue(len(result) != 0)
        self.assertEqual(len(result), end - start)
        self.assertEqual(type(result), type([]))

    def test_search_character(self):
        results = self.scraper.search_character('mitsuha')
        self.assertEqual(type(results), type([]))
        self.assertLessEqual(len(results), 5)

    def test_get_character(self):
        result = self.scraper.get_character('mitsuha')
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.name)

    def test_get_all_character(self):
        start = 0
        end = 50
        results = self.scraper.get_all_characters(start=start, end=end)

        self.assertNotEqual(len(results), 0)
        self.assertEqual(len(results), end - start)
        self.assertEqual(type(results), type([]))


if __name__ == '__main__':
    unittest.main()
