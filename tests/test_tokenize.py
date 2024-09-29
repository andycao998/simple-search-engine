from unittest import TestCase
from tokenizer import tokenize


class Test(TestCase):
    def test_tokenize_splits_on_space(self):
        self.assertEqual(['some', 'word'], tokenize('some word'))

    def test_tokenize_lowercase(self):
        self.assertEqual(['some', 'word'], tokenize('SoMe WoRD'))

    def test_tokenize_separate_period(self):
        self.assertEqual(['some', 'sentence', '.'], tokenize('some sentence.'))

    # TODO: Implement in next version
    # def test_tokenize_period_in_abbreviations(self):
    #    self.assertEqual(['dr.', 'brown'], tokenize('Dr. Brown'))

    def test_tokenize_split_comma(self):
        self.assertEqual(['some', ',', 'word'], tokenize('some, word'))
