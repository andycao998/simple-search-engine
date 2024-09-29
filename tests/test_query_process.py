from unittest import TestCase
from query_process import parse_phrases


class Test(TestCase):
    def test_parse_phrases_one_term(self):
        self.assertEqual({0: ['orange']}, parse_phrases(['"orange"']))

    def test_parse_phrases_two_terms(self):
        self.assertEqual({0: ['orange', 'fruit']}, parse_phrases(['"orange', 'fruit"']))

    def test_parse_phrases_three_terms(self):
        self.assertEqual({0: ['blue', 'cotton', 'shirt']}, parse_phrases(['"blue', 'cotton', 'shirt"']))

    def test_parse_phrases_two_phrases(self):
        self.assertEqual({0: ['orange', 'fruit'], 1: ['vitamin', 'c']},
                         parse_phrases(['"orange', 'fruit"', '"vitamin', 'c"']))

    def test_parse_phrases_phrase_term_combo(self):
        self.assertEqual({0: ['orange', 'fruit']}, parse_phrases(['"orange', 'fruit"', 'hungry']))

    def test_parse_phrases_no_phrase(self):
        self.assertEqual({}, parse_phrases(['yellow', 'lemon']))
