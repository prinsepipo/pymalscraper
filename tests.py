import unittest

from pymalscraper.scraper import MALScraper
from pymalscraper.models import Anime


class MALScraperTest(unittest.TestCase):
    def setUp(self) -> None:
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

    def test_anime_list_are_anime_objects(self):
        anime_list = self.scraper.get_anime_list(0, 20)

        for anime in anime_list:
            self.assertEqual(Anime, type(anime))

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


class AnimeModelTest(unittest.TestCase):

    def setUp(self):
        self.anime = Anime('https://myanimelist.net/anime/32281/Kimi_no_Na_wa')

    def test_anime_has_title(self):
        self.assertEqual(self.anime.title, 'Kimi no Na wa.')

    def test_anime_has_english_title(self):
        self.assertEqual(self.anime.english_title, 'Your Name.')

    def test_anime_has_japanese_title(self):
        self.assertEqual(self.anime.japanese_title, '君の名は。')

    def test_anime_has_no_synonyms(self):
        self.assertIsNone(self.anime.synonyms)

    def test_anime_has_synopsis(self):
        self.assertIsNotNone(self.anime.synopsis)

    def test_anime_has_animetype(self):
        self.assertEqual(self.anime.animetype, 'Movie')

    def test_anime_has_episodes(self):
        self.assertEqual(self.anime.episodes, '1')

    def test_anime_has_genres(self):
        self.assertListEqual(self.anime.genres, [
            'Romance', 'Supernatural', 'School', 'Drama'])

    def test_anime_has_poster(self):
        self.assertEqual(
            self.anime.poster, 'https://cdn.myanimelist.net/images/anime/5/87048.jpg')

    def test_anime_has_trailer(self):
        self.assertEqual(
            self.anime.trailer, 'https://www.youtube.com/embed/3KR8_igDs1Y?enablejsapi=1&wmode=opaque&autoplay=1')
