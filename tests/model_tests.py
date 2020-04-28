import unittest

from pymalscraper.models import Anime


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
