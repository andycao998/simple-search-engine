import collections
import json
import math

from documents import TransformedDocument
from index import BaseIndex


def count_terms(term_list: list[str]) -> collections.Counter:
    # print(collections.Counter(term_list))
    return collections.Counter(term_list)


class TfIdfInvertedIndex(BaseIndex):
    def __init__(self):
        self.doc_counts = collections.Counter()
        self.term_to_doc_id_tf_scores: dict[str, dict[str, float]] = collections.defaultdict(dict)
        self.total_documents_count = 0

    def add_document(self, doc: TransformedDocument):
        # term_counts = count_terms(doc.terms)
        # # self.doc_counts.update(term_counts.keys())
        # self.total_documents_count += 1
        #
        # for doc_term in term_counts.keys():
        #     self.term_to_doc_id_tf_scores[doc_term][doc.doc_id] = term_counts.items()
        #     term_count = 0
        #     total_terms = 0
        #     if doc.doc_id in self.term_to_doc_id_tf_scores.get(doc_term):
        #         items = self.term_to_doc_id_tf_scores[doc_term][doc.doc_id]
        #         for item in items:
        #             total_terms += item[1]
        #             if item[0] == doc_term:
        #                 term_count = item[1]
        #
        #     term_frequency = 0
        #     if total_terms != 0:
        #         term_frequency = term_count / total_terms
        #     self.term_to_doc_id_tf_scores[doc_term][doc.doc_id] = term_frequency
        term_counts = count_terms(doc.terms)
        # print(term_counts)
        # print(len(term_counts))
        self.total_documents_count += 1
        total_terms = 0

        for item in term_counts.items():
            total_terms += item[1]

        for doc_term, term_count in term_counts.items():
            term_frequency = term_count / total_terms
            self.term_to_doc_id_tf_scores[doc_term][doc.doc_id] = term_frequency

    def term_frequency(self, term, doc_id: str):
        if self.term_to_doc_id_tf_scores[term].get(doc_id) is None:
            return 0
        return self.term_to_doc_id_tf_scores[term][doc_id]

    def inverse_document_frequency(self, set_of_docs_len):
        # return self.total_documents_count / self.doc_counts[term]
        # print(self.total_documents_count)
        # print(set_of_docs_len)
        return math.log(self.total_documents_count / set_of_docs_len)

    def tf_idf(self, term, doc_id, set_of_docs_len):
        # print(self.term_frequency(term, doc_id))
        # print(self.inverse_document_frequency(term, set_of_docs_len))
        return self.term_frequency(term, doc_id) * self.inverse_document_frequency(set_of_docs_len)

    def combine_term_scores(self, term_list: list[str], doc_id, set_of_docs_len) -> int:
        return sum([self.tf_idf(term, doc_id, set_of_docs_len) for term in term_list])

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        scores = dict()
        set_of_docs = set()

        for term in processed_query:
            if self.term_to_doc_id_tf_scores.get(term) is not None:
                new_set = set(self.term_to_doc_id_tf_scores.get(term).keys())
                # print(new_set)
                if len(set_of_docs) == 0:
                    set_of_docs = new_set  # set_of_docs.union(new_set)
                else:
                    set_of_docs = set_of_docs.intersection(new_set)
            else:
                # all terms must be present in a document to count
                set_of_docs = set()
                break

        # print(set_of_docs)
        # print(self.total_documents_count)
        for doc in set_of_docs:
            doc_id = doc
            score = self.combine_term_scores(processed_query, doc_id, len(set_of_docs))
            scores[doc_id] = score
        print(scores)
        return sorted(scores.keys(), key=scores.get, reverse=True)[:number_of_results]

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
            for doc_id, counts in self.term_to_doc_id_tf_scores.items():
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
