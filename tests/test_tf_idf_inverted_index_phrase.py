from unittest import TestCase
from documents import TransformedDocument
from tf_idf_inverted_index_phrase import TfIdfInvertedIndexPhrase
from query_process import parse_phrases


def strip_query_quotes(query: list[str]) -> list[str]:
    query_quotes_removed = []
    for term in query:
        term = term.lstrip('"')
        term = term.rstrip('"')
        query_quotes_removed.append(term)
    return query_quotes_removed


class TestTfIdfInvertedIndexPhrase(TestCase):
    def test_index_term_positions(self):
        # documents should be tokenized: lowercase
        first = TransformedDocument(doc_id='1', terms=['chicago', 'houston', 'la', 'houston'])
        second = TransformedDocument(doc_id='2', terms=['baltimore', 'orlando', 'houston'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        list_of_docs = [first, second, third]
        index = TfIdfInvertedIndexPhrase()

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        self.assertEqual([0], index.term_to_doc_id_tf_scores['chicago']['1']['indexes'])
        self.assertEqual([1, 3], index.term_to_doc_id_tf_scores['houston']['1']['indexes'])
        self.assertEqual([2], index.term_to_doc_id_tf_scores['houston']['2']['indexes'])
        self.assertEqual([2], index.term_to_doc_id_tf_scores['la']['1']['indexes'])
        self.assertEqual([0], index.term_to_doc_id_tf_scores['baltimore']['2']['indexes'])
        self.assertEqual([1], index.term_to_doc_id_tf_scores['orlando']['2']['indexes'])
        self.assertEqual([0], index.term_to_doc_id_tf_scores['washington']['3']['indexes'])
        self.assertEqual([1], index.term_to_doc_id_tf_scores['is']['3']['indexes'])
        self.assertEqual([2], index.term_to_doc_id_tf_scores['a']['3']['indexes'])
        self.assertEqual([3], index.term_to_doc_id_tf_scores['state']['3']['indexes'])
        self.assertEqual([4], index.term_to_doc_id_tf_scores['in']['3']['indexes'])
        self.assertEqual([5], index.term_to_doc_id_tf_scores['the']['3']['indexes'])
        self.assertEqual([6], index.term_to_doc_id_tf_scores['us']['3']['indexes'])

    def test_search_one_match(self):
        index = TfIdfInvertedIndexPhrase()
        first = TransformedDocument(doc_id='1', terms=['chicago', 'is', 'a', 'city', 'in', 'illinois'])
        second = TransformedDocument(doc_id='2', terms=['america', 'declared', 'independence', 'with', 'the',
                                                        'declaration', 'of', 'independence'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        fourth = TransformedDocument(doc_id='4', terms=['oranges', 'contain', 'vitamin', 'c'])
        fifth = TransformedDocument(doc_id='5', terms=['thanksgiving', 'is', 'celebrated', 'in', 'the', 'us'])
        sixth = TransformedDocument(doc_id='6', terms=['mangoes', 'contain', 'vitamin', 'a'])
        seventh = TransformedDocument(doc_id='7', terms=['aurora', 'is', 'a', 'city', 'in', 'illinois'])
        eighth = TransformedDocument(doc_id='8', terms=['joliet', 'is', 'a', 'city', 'in', 'illinois'])
        ninth = TransformedDocument(doc_id='9', terms=['thomas', 'jefferson', 'helped', 'write', 'the',
                                                       'declaration', 'of', 'independence'])
        tenth = TransformedDocument(doc_id='10', terms=['fossil', 'fuels', 'are', 'damaging', 'to', 'the',
                                                        'environment'])
        list_of_docs = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
        query = ['fossil', 'fuels']

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        number_of_results = 10
        phrase_dict = parse_phrases(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = ['10']
        self.assertEqual(result, outcome)

    def test_search_multiple_matches(self):
        index = TfIdfInvertedIndexPhrase()
        first = TransformedDocument(doc_id='1', terms=['chicago', 'is', 'the', 'largest', 'city', 'in', 'illinois'])
        second = TransformedDocument(doc_id='2', terms=['america', 'declared', 'independence', 'with', 'the',
                                                        'declaration', 'of', 'independence'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        fourth = TransformedDocument(doc_id='4', terms=['oranges', 'contain', 'vitamin', 'c'])
        fifth = TransformedDocument(doc_id='5', terms=['thanksgiving', 'is', 'celebrated', 'in', 'the', 'us'])
        sixth = TransformedDocument(doc_id='6', terms=['mangoes', 'contain', 'vitamin', 'a'])
        seventh = TransformedDocument(doc_id='7', terms=['aurora', 'is', 'a', 'city', 'in', 'illinois'])
        eighth = TransformedDocument(doc_id='8', terms=['joliet', 'is', 'a', 'city', 'in', 'illinois', 'with', 'stuff'])
        ninth = TransformedDocument(doc_id='9', terms=['thomas', 'jefferson', 'helped', 'write', 'the',
                                                       'declaration', 'of', 'independence'])
        tenth = TransformedDocument(doc_id='10', terms=['fossil', 'fuels', 'are', 'damaging', 'to', 'the',
                                                        'environment'])
        list_of_docs = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
        query = ['"city', 'in', 'illinois"']

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        number_of_results = 10
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)

        # scoring isn't tested so lists are sorted just to match the documents without failing tests because of order
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['1', '7', '8'])
        self.assertEqual(result, outcome)

        query = ['"contain', 'vitamin"']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['4', '6'])
        self.assertEqual(result, outcome)

        query = ['"declaration', 'of', 'independence"']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['2', '9'])
        self.assertEqual(result, outcome)

        query = ['"in', 'the', 'us"']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['3', '5'])
        self.assertEqual(result, outcome)

    def test_search_no_matches(self):
        index = TfIdfInvertedIndexPhrase()
        first = TransformedDocument(doc_id='1', terms=['chicago', 'is', 'the', 'largest', 'city', 'in', 'illinois'])
        second = TransformedDocument(doc_id='2', terms=['america', 'declared', 'independence', 'with', 'the',
                                                        'declaration', 'of', 'independence'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        fourth = TransformedDocument(doc_id='4', terms=['oranges', 'contain', 'vitamin', 'c'])
        fifth = TransformedDocument(doc_id='5', terms=['thanksgiving', 'is', 'celebrated', 'in', 'the', 'us'])
        sixth = TransformedDocument(doc_id='6', terms=['mangoes', 'contain', 'vitamin', 'a'])
        seventh = TransformedDocument(doc_id='7', terms=['aurora', 'is', 'a', 'city', 'in', 'illinois'])
        eighth = TransformedDocument(doc_id='8', terms=['joliet', 'is', 'a', 'city', 'in', 'illinois', 'with', 'stuff'])
        ninth = TransformedDocument(doc_id='9', terms=['thomas', 'jefferson', 'helped', 'write', 'the',
                                                       'declaration', 'of', 'independence'])
        tenth = TransformedDocument(doc_id='10', terms=['fossil', 'fuels', 'are', 'damaging', 'to', 'the',
                                                        'environment'])
        list_of_docs = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
        query = ['"cities', 'in', 'illinois"']

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        number_of_results = 10
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = []
        self.assertEqual(result, outcome)

        query = ['"contains', 'vitamin"']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = []
        self.assertEqual(result, outcome)

        query = ['"declaration', 'independence"']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = []
        self.assertEqual(result, outcome)

        query = ['"chicago', 'locations"']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = []
        self.assertEqual(result, outcome)

    def test_search_multiple_queries(self):
        index = TfIdfInvertedIndexPhrase()
        first = TransformedDocument(doc_id='1', terms=['chicago', 'is', 'the', 'largest', 'city', 'in', 'illinois'])
        second = TransformedDocument(doc_id='2', terms=['america', 'declared', 'independence', 'with', 'the',
                                                        'declaration', 'of', 'independence'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        fourth = TransformedDocument(doc_id='4', terms=['oranges', 'contain', 'vitamin', 'c'])
        fifth = TransformedDocument(doc_id='5', terms=['thanksgiving', 'is', 'celebrated', 'in', 'the', 'us'])
        sixth = TransformedDocument(doc_id='6', terms=['mangoes', 'contain', 'vitamin', 'a'])
        seventh = TransformedDocument(doc_id='7', terms=['aurora', 'is', 'a', 'city', 'in', 'illinois'])
        eighth = TransformedDocument(doc_id='8', terms=['joliet', 'is', 'a', 'city', 'in', 'illinois', 'with', 'stuff'])
        ninth = TransformedDocument(doc_id='9', terms=['thomas', 'jefferson', 'helped', 'write', 'the',
                                                       'declaration', 'of', 'independence'])
        tenth = TransformedDocument(doc_id='10', terms=['fossil', 'fuels', 'are', 'damaging', 'to', 'the',
                                                        'environment'])
        list_of_docs = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
        query = ['"in', 'illinois"', '"a', 'city"']

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        number_of_results = 10
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['7', '8'])
        self.assertEqual(result, outcome)

    def test_search_phrase_term_combo(self):
        index = TfIdfInvertedIndexPhrase()
        first = TransformedDocument(doc_id='1', terms=['chicago', 'is', 'the', 'largest', 'city', 'in', 'illinois'])
        second = TransformedDocument(doc_id='2', terms=['america', 'declared', 'independence', 'with', 'the',
                                                        'declaration', 'of', 'independence'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        fourth = TransformedDocument(doc_id='4', terms=['oranges', 'contain', 'vitamin', 'c'])
        fifth = TransformedDocument(doc_id='5', terms=['thanksgiving', 'is', 'celebrated', 'in', 'the', 'us'])
        sixth = TransformedDocument(doc_id='6', terms=['mangoes', 'contain', 'vitamin', 'a'])
        seventh = TransformedDocument(doc_id='7', terms=['aurora', 'is', 'a', 'city', 'in', 'illinois'])
        eighth = TransformedDocument(doc_id='8', terms=['joliet', 'is', 'a', 'city', 'in', 'illinois', 'with', 'stuff'])
        ninth = TransformedDocument(doc_id='9', terms=['thomas', 'jefferson', 'helped', 'write', 'the',
                                                       'declaration', 'of', 'independence'])
        tenth = TransformedDocument(doc_id='10', terms=['fossil', 'fuels', 'are', 'damaging', 'to', 'the',
                                                        'environment'])
        list_of_docs = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
        query = ['"in', 'illinois"', 'largest']

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        number_of_results = 10
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = ['1']
        self.assertEqual(result, outcome)

        query = ['"declaration', 'of', 'independence"', 'declared']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = index.search(query, phrase_dict, number_of_results)
        outcome = ['2']
        self.assertEqual(result, outcome)

    def test_search_no_phrases(self):
        index = TfIdfInvertedIndexPhrase()
        first = TransformedDocument(doc_id='1', terms=['chicago', 'is', 'the', 'largest', 'city', 'in', 'illinois'])
        second = TransformedDocument(doc_id='2', terms=['america', 'declared', 'independence', 'with', 'the',
                                                        'declaration', 'of', 'independence'])
        third = TransformedDocument(doc_id='3', terms=['washington', 'is', 'a', 'state', 'in', 'the', 'us'])
        fourth = TransformedDocument(doc_id='4', terms=['oranges', 'contain', 'vitamin', 'c'])
        fifth = TransformedDocument(doc_id='5', terms=['thanksgiving', 'is', 'celebrated', 'in', 'the', 'us'])
        sixth = TransformedDocument(doc_id='6', terms=['mangoes', 'contain', 'vitamin', 'a'])
        seventh = TransformedDocument(doc_id='7', terms=['aurora', 'is', 'a', 'city', 'in', 'illinois'])
        eighth = TransformedDocument(doc_id='8', terms=['joliet', 'is', 'a', 'city', 'in', 'illinois', 'with', 'stuff'])
        ninth = TransformedDocument(doc_id='9', terms=['thomas', 'jefferson', 'helped', 'write', 'the',
                                                       'declaration', 'of', 'independence'])
        tenth = TransformedDocument(doc_id='10', terms=['fossil', 'fuels', 'are', 'damaging', 'to', 'the',
                                                        'environment'])
        list_of_docs = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
        query = ['illinois', 'city']

        for doc in list_of_docs:
            index.add_document(doc)
            index.index_term_positions(doc)

        number_of_results = 10
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['1', '7', '8'])
        self.assertEqual(result, outcome)

        query = ['declaration', 'independence']
        phrase_dict = parse_phrases(query)
        query = strip_query_quotes(query)
        result = sorted(index.search(query, phrase_dict, number_of_results))
        outcome = sorted(['2', '9'])
        self.assertEqual(result, outcome)
