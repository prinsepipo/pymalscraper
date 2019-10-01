import unittest

from pymalscraper.scraper import Scraper


class ScraperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper()

    def test_get_all_anime(self):
        start = 0
        end = 50
        anime_list = self.scraper.get_all_anime(start, end)
        self.assertEqual(len(anime_list), end - start)

        for anime in anime_list:
            # These are important factors. Every anime has these.
            self.assertIsNotNone(anime.title)
            self.assertIsNotNone(anime.poster)

    def test_get_anime(self):
        anime = self.scraper.get_anime("kimi no na wa")
        self.assertIsNotNone(anime.title)
        self.assertIsNotNone(anime.poster)
        self.assertIn(self.scraper.BASE_URL, anime.url)

        # Invalid.
        with self.assertRaises(TypeError):
            self.scraper.get_anime(21)
            self.scraper.get_anime(["kimi no na wa"])
            self.scraper.get_anime(("kimi no na wa",))

    def test_search_anime(self):
        results = self.scraper.search_anime("sword art online")
        self.assertLessEqual(len(results), 5)
        self.assertNotEqual(len(results), 0)

        for result in results:
            self.assertIs(type(result), tuple)
            self.assertIsNotNone(result[0])
            self.assertIsNotNone(result[1])
            self.assertIn(self.scraper.BASE_URL, result[1])

        # MAL requires query to have at least 3 byte characters to search.
        results = self.scraper.search_anime('re')
        self.assertEqual(len(results), 0)

    def test_get_all_characters(self):
        start = 0
        end = 50
        character_list = self.scraper.get_all_characters(start, end)
        self.assertEqual(len(character_list), end - start)

        for character in character_list:
            self.assertIsNotNone(character.name)
            self.assertIsNotNone(character.poster)
            gallery = character.get_gallery()
            self.assertNotEqual(len(gallery), 0)

            for image in gallery:
                self.assertIn('https', image)

    def test_get_character(self):
        character = self.scraper.get_character('lelouch lamperouge')
        self.assertIsNotNone(character)
        self.assertIsNotNone(character.name)
        self.assertIsNotNone(character.alternate_names)
        self.assertIsNotNone(character.poster)
        gallery = character.get_gallery()
        self.assertNotEqual(len(gallery), 0)

        # Invalid.
        with self.assertRaises(TypeError):
            self.scraper.get_character(9)
            self.scraper.get_character(['lelouch lamperouge'])
            self.scraper.get_character(('lelouch lamperouge',))

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
        results = self.scraper.search_character('02')
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
