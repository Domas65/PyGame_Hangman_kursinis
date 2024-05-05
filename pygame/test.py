import unittest
from main import HangmanGame

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.game = HangmanGame()

    def test_open_word_list(self):
        # Test opening word list for English
        english_words = self.game.open_word_list("english")
        self.assertTrue(english_words)
        self.assertIsInstance(english_words, list)

        # Test opening word list for Lietuvių
        lietuviu_words = self.game.open_word_list("Lietuvių")
        self.assertTrue(lietuviu_words)
        self.assertIsInstance(lietuviu_words, list)

    def test_separate_word(self):
        # Test separating a word
        word = "test"
        separated_word = self.game.separate_word(word)
        self.assertEqual(separated_word, ['t', 'e', 's', 't'])

    def test_hide_word(self):
        # Test hiding a word
        separated_word = ['t', 'e', 's', 't']
        hidden_word = self.game.hide_word(separated_word)
        self.assertEqual(hidden_word, ['_', '_', '_', '_'])

    def test_reveal_letter(self):
        self.game.random_word = "test"
        self.game.hidden_word = ['_', '_', '_', '_']  
        revealed = self.game.reveal_letter('t')
        self.assertTrue(revealed)
        self.assertEqual(self.game.hidden_word, ['t', '_', '_', 't'])
        revealed = self.game.reveal_letter('x')
        self.assertFalse(revealed)
        self.assertIn('x', self.game.missed_letters)



if __name__ == '__main__':
    unittest.main()
