from unittest import TestCase
import search


class Test(TestCase):
    def test_match_true(self):
        self.assertTrue(search.match(document='red and blue', query='red'))

    def test_match_false(self):
        self.assertFalse(search.match(document='yellow and re', query='red'))

    def test_match_strange_true(self):
        self.assertTrue(search.match(document='predict', query='red'))

    def test_match_multiple_terms_true(self):
        self.assertTrue(search.match(document='see the next day', query='see the'))

    def test_match_multiple_terms_false(self):
        self.assertFalse(search.match(document='i see the house', query='see  the'))

    def test_match_empty_query_true(self):
        self.assertTrue(search.match(document='predict', query=''))

    def test_match_empty_document_false(self):
        self.assertFalse(search.match(document='', query=' '))

    def test_boolean_term_match_true(self):
        self.assertTrue(search.boolean_term_match(document='red and blue', query='red'))

    def test_boolean_term_match_false(self):
        self.assertFalse(search.boolean_term_match(document='yellow and blue', query='red'))

    def test_boolean_term_match_strange_false(self):
        self.assertFalse(search.boolean_term_match(document='red. and blue', query='red'))

    def test_boolean_term_match_multiple_terms_true(self):
        self.assertTrue(search.boolean_term_match(document='red and blue', query='red blue'))

    def test_boolean_term_match_multiple_terms_false(self):
        self.assertFalse(search.boolean_term_match(document='red blue', query='red and blue'))

    def test_boolean_term_match_empty_query_true(self):
        self.assertTrue(search.boolean_term_match(document='red blue', query=''))

    def test_boolean_term_match_empty_document_strange_true(self):  # query is split into empty strings, which matches
        self.assertTrue(search.boolean_term_match(document='', query='    '))

    def test_boolean_term_match_empty_document_false(self):
        self.assertFalse(search.boolean_term_match(document='', query='...'))

    def test_search(self):
        self.assertEqual(['red and blue', 'yellow and red'],
                         search.search(query='red', documents=['red and blue', 'red. blue blue',
                                                               'yellow and red']))

    def test_search_empty_query(self):
        self.assertEqual(['red and blue', 'red. blue blue', 'yellow and red'],
                         search.search(query='', documents=['red and blue', 'red. blue blue',
                                                            'yellow and red']))

    def test_search_empty_document(self):
        self.assertEqual([], search.search(query='red and blue', documents=[]))
# tab copy path absolute path
