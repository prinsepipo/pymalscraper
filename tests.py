import unittest

from pymalscraper.scraper import Scraper


class ScraperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper()

    def test_search_anime(self):
        results = self.scraper.search_anime('sword art online')
        self.assertLessEqual(len(results), 5)

        for result in results:
            self.assertIs(type(result), tuple)
            self.assertIsNotNone(result[0])
            self.assertIsNotNone(result[1])
            self.assertIn(self.scraper.BASE_URL, result[1])

        # MAL requires query to have at least 3 byte characters to search.
        with self.assertRaises(ValueError):
            self.scraper.search_anime('re')

        with self.assertRaises(TypeError):
            self.scraper.search_anime(100)

    def test_get_anime(self):
        anime = self.scraper.get_anime('kimi no nawa')
        self.assertIsNotNone(anime.title)
        self.assertIsNotNone(anime.poster)
        self.assertIsNotNone(anime.synopsis)

        # Invalid inputs.
        with self.assertRaises(TypeError):
            self.scraper.get_anime(21)
            self.scraper.get_anime(['kimi no na wa'])
            self.scraper.get_anime(('kimi no na wa',))

    def test_get_all_anime(self):
        start = 0
        end = 50
        anime_list = self.scraper.get_all_anime(start, end)
        self.assertEqual(len(anime_list), end - start)

        for anime in anime_list:
            data = anime.get_data()
            self.assertIsNotNone(data)

    def test_search_character(self):
        results = self.scraper.search_character('zero two')
        self.assertLessEqual(len(results), 5)
        self.assertNotEqual(len(results), 0)

        for result in results:
            self.assertIs(type(result), tuple)
            self.assertIsNotNone(result[0])
            self.assertIsNotNone(result[1])
            self.assertIn(self.scraper.BASE_URL, result[1])

        # MAL requires query to have at least 3 byte characters to search.
        with self.assertRaises(ValueError):
            self.scraper.search_character('02')

        with self.assertRaises(TypeError):
            self.scraper.search_anime(1061811)

    def test_get_character(self):
        character = self.scraper.get_character('lelouch lamperouge')
        self.assertIsNotNone(character)
        self.assertIsNotNone(character.name)
        self.assertIsNotNone(character.alternate_names)
        self.assertIsNotNone(character.poster)
        gallery = character.get_gallery()
        self.assertNotEqual(len(gallery), 0)

        # Invalid inputs.
        with self.assertRaises(TypeError):
            self.scraper.get_character(9)
            self.scraper.get_character(['lelouch lamperouge'])
            self.scraper.get_character(('lelouch lamperouge',))

    def test_get_all_characters(self):
        start = 0
        end = 25
        character_list = self.scraper.get_all_characters(start, end)
        self.assertEqual(len(character_list), end - start)

        with self.assertRaises(ValueError):
            self.scraper.get_all_characters(end, start)


if __name__ == '__main__':
    unittest.main()
