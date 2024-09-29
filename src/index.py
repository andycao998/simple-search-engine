import collections

from documents import TransformedDocument


def count_terms(term_list: list[str]) -> dict[str, int]:
    term_counts_dict = collections.defaultdict(int)
    for term in term_list:
        term_counts_dict[term] += 1
    return term_counts_dict


def combine_term_scores(term_list: list[str], term_counts_dict: dict[str, int]) -> int:
    term_sum = 0
    for term in term_list:
        if term in term_counts_dict:
            term_sum += term_counts_dict.get(term)
    return term_sum


class BaseIndex:
    def add_document(self, doc: TransformedDocument):
        pass

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        pass


class Index(BaseIndex):
    def __init__(self):
        # dict[str, dict[str, int]]
        self.id_to_terms_counts = dict()

    def add_document(self, doc: TransformedDocument):
        self.id_to_terms_counts[doc.doc_id] = count_terms(doc.terms)

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        # mapping from doc_ids to term counts in the corresponding document
        # straight term count relevance
        scores = dict()
        # id_to_terms_combined_counts = collections.defaultdict(int)
        for doc_id in self.id_to_terms_counts.keys():
            score = combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        return sorted(self.id_to_terms_counts.keys(), key=scores.get, reverse=True)[:number_of_results]

