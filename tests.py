import unittest

from pymalscraper.scraper import Scraper


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
        self.assertEqual(len(results), 5)


if __name__ == '__main__':
    unittest.main()
