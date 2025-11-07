import unittest
from src.data_utils import clean_text

class TestDataUtils(unittest.TestCase):
    
    def test_clean_text(self):
        #emoji normalization
        self.assertEqual(clean_text('project 🙂‍↕️🙂‍↕️ Icarus  🙂‍↕️ '), 'project Icarus', 'Did not remove emojis')
        #leading whitespace normalization
        self.assertEqual(clean_text('  Hey  there  '), 'Hey there', 'Did not normalize leading whitespaces properly')
        #exclamation normalization
        self.assertEqual(clean_text('Nice to meet you!!!'), 'Nice to meet you!', 'Did not normalize "!" number properly')
        #space normalization
        self.assertEqual(clean_text('Hey  there  friend'), 'Hey there friend', 'Did not normalize " " properly')
        #tab normalization
        self.assertEqual(clean_text('       Hey         there   '), 'Hey there', 'Did not normalize \\t, "    " properly')
        #paragraph break normalization
        self.assertEqual(clean_text('Hey\n    \n\n\n there'), 'Hey\n\n there', 'Did not normalize \\n, newline characters properly')
        #mutliple comma normalization
        self.assertEqual(clean_text('Hey,, there'), 'Hey, there', 'Did not normalize comma, "," properly')
        #multiple periods normalization
        self.assertEqual(clean_text('Hey there....'), 'Hey there.', 'Did not normalize number of periods properly')