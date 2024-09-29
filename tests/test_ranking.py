from unittest import TestCase
import ranking


class Test(TestCase):
    def test_term_count_relevance_single_term_query(self):
        self.assertEqual(2, ranking.term_count_relevance(document='red is a color. red is great', query='red'))

    def test_term_count_relevance_multiple_term_query(self):
        self.assertEqual(3, ranking.term_count_relevance(document='red is a color . red is great',
                         query='red color'))

    def test_term_count_relevance_partial_match(self):
        self.assertEqual(2, ranking.term_count_relevance(document='red is a color . red is great',
                         query='red and blue'))

    def test_term_count_relevance_empty_query(self):
        self.assertEqual(0, ranking.term_count_relevance(document='red is a color . red is great', query=''))

    def test_term_count_relevance_empty_document(self):
        self.assertEqual(0, ranking.term_count_relevance(document='', query='red'))

    def test_boolean_term_count_relevance_single_term_query(self):
        self.assertEqual(1, ranking.boolean_term_count_relevance(document='red is a color. red is great',
                         query='red'))

    def test_boolean_term_count_relevance_multiple_term_query(self):
        self.assertEqual(2, ranking.boolean_term_count_relevance(document='red is a color . red is great',
                         query='red color'))

    def test_boolean_term_count_relevance_partial_match(self):
        self.assertEqual(1, ranking.boolean_term_count_relevance(document='red is a color. red is great',
                         query='red and blue'))

    def test_boolean_term_count_relevance_empty_query(self):
        self.assertEqual(0, ranking.boolean_term_count_relevance(document='red is a color. red is great', query=''))

    def test_boolean_term_count_relevance_empty_document(self):
        self.assertEqual(0, ranking.boolean_term_count_relevance(document='', query='pizza'))

    def test_search2(self):
        self.assertEquals(['blue red red apple', 'red color minus blue', 'cheese'],
                          ranking.search2(documents=['red color minus blue', 'cheese', 'blue red red apple'],
                                          query='red blue'))

    def test_search2_empty_query(self):
        self.assertEquals(['red color minus blue', 'cheese', 'blue red red apple'],
                          ranking.search2(documents=['red color minus blue', 'cheese', 'blue red red apple'], query=''))

    def test_search2_empty_document(self):
        self.assertEquals([], ranking.search2(documents=[], query='red and blue'))
