import collections
import json
import math

from documents import TransformedDocument
from index import BaseIndex


def count_terms(term_list: list[str]) -> collections.Counter:
    # print(collections.Counter(term_list))
    return collections.Counter(term_list)
    # term_counts_dict = collections.defaultdict(int)
    # for term in term_list:
    #     term_counts_dict[term] += 1
    # return term_counts_dict


class TfIdfIndex(BaseIndex):
    def __init__(self):
        # mapping of terms to the number of documents they occur in
        self.doc_counts = collections.Counter()
        self.id_to_terms_counts: dict[str, collections.Counter] = dict()

    def add_document(self, doc: TransformedDocument):
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())
        self.id_to_terms_counts[doc.doc_id] = term_counts

    def term_frequency(self, term, doc_id):
        return self.id_to_terms_counts[doc_id][term] / sum(self.id_to_terms_counts[doc_id].values())

    def inverse_document_frequency(self, term):
        return math.log(len(self.id_to_terms_counts) / self.doc_counts[term])

    def tf_idf(self, term, doc_id):
        if term in self.doc_counts:
            return self.term_frequency(term, doc_id) * self.inverse_document_frequency(term)
        return 0

    def combine_term_scores(self, term_list: list[str], doc_id) -> int:
        return sum([self.tf_idf(term, doc_id) for term in term_list])

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        # mapping from doc_ids to term counts in the corresponding document
        # straight term count relevance
        scores = dict()
        # id_to_terms_combined_counts = collections.defaultdict(int)
        for doc_id in self.id_to_terms_counts.keys():
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        # print(scores)
        return sorted(self.id_to_terms_counts.keys(), key=scores.get, reverse=True)[:number_of_results]

        # query_terms_set = set(processed_query)
        # results = []
        # for doc_id, doc_term_set in self.id_to_terms_counts.items():
        #     if query_terms_set.issubset(doc_term_set):
        #         results.append(doc_id)
        # TODO: Make results into a class.
        # return results

    def write(self, path: str):
        with open(path, 'w') as fp:
            fp.write(json.dumps({
                '__metadata__': {
                    'doc_counts': [
                        {
                            'term': term,
                            'count': count
                        }
                        for term, count in self.doc_counts.items()
                    ]
                }
            }) + '\n')
            for doc_id, counts in self.id_to_terms_counts.items():
                fp.write(json.dumps({
                    'doc_id': doc_id,
                    'counts': [
                        {
                            'term': term,
                            'count': count
                        }
                        for term, count in counts.items()
                    ]
                }) + '\n')
