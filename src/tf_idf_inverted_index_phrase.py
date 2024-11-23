import collections
import json
import math

from documents import TransformedDocument
from index import BaseIndex
from collections import defaultdict

def count_terms(term_list: list[str]) -> collections.Counter:
    return collections.Counter(term_list)

class TfIdfInvertedIndexPhrase(BaseIndex):
    def __init__(self):
        self.doc_counts = collections.Counter()
        # Each term in the query is mapped to a dictionary containing each document and its tf_idf score and the indexes where the term occurs in the document
        self.term_to_doc_id_tf_scores: dict[str, dict[str, dict[float, list[int]]]] = defaultdict(lambda: defaultdict(dict))
        self.total_documents_count = 0

    def index_term_positions(self, doc: TransformedDocument):
        for i, term in enumerate(doc.terms):
            if len(self.term_to_doc_id_tf_scores[term][doc.doc_id]) == 1:
                self.term_to_doc_id_tf_scores[term][doc.doc_id]['indexes'] = []
            self.term_to_doc_id_tf_scores[term][doc.doc_id]['indexes'].append(i)

    def add_document(self, doc: TransformedDocument):
        term_counts = count_terms(doc.terms)
        self.total_documents_count += 1
        total_terms = 0

        for item in term_counts.items():
            total_terms += item[1]

        for doc_term, term_count in term_counts.items():
            if self.term_to_doc_id_tf_scores[doc_term][doc.doc_id] is None:
                self.term_to_doc_id_tf_scores[doc_term][doc.doc_id] = dict()
            term_frequency = term_count / total_terms
            self.term_to_doc_id_tf_scores[doc_term][doc.doc_id]['frequency'] = term_frequency

    def term_frequency(self, term, doc_id: str):
        if self.term_to_doc_id_tf_scores[term].get(doc_id) is None:
            return 0
        return self.term_to_doc_id_tf_scores[term][doc_id]['frequency']

    def inverse_document_frequency(self, set_of_docs_len):
        return math.log(self.total_documents_count / set_of_docs_len)

    def tf_idf(self, term, doc_id, set_of_docs_len):
        return self.term_frequency(term, doc_id) * self.inverse_document_frequency(set_of_docs_len)

    def combine_term_scores(self, term_list: list[str], doc_id, set_of_docs_len) -> int:
        return sum([self.tf_idf(term, doc_id, set_of_docs_len) for term in term_list])

    def search(self, processed_query: list[str], phrase_dict: dict[int, list[str]], number_of_results: int) -> list[str]:
        scores = dict()
        set_of_docs = set()
        first_term = True

        for term in processed_query:
            if self.term_to_doc_id_tf_scores.get(term) is not None:
                new_set = set(self.term_to_doc_id_tf_scores.get(term).keys())

                if len(set_of_docs) == 0 and first_term:
                    set_of_docs = new_set  
                    first_term = False
                else:
                    set_of_docs = set_of_docs.intersection(new_set)
            else:
                # All terms must be present in a document to count
                set_of_docs = set()
                break
        
        # valid_docs = set()
        # for doc in set_of_docs:
        #     phrase_in_doc = True
        #     for phrase_list in phrase_dict.values():  # Loop if there are multiple separate phrases in query
        #         for i, term in enumerate(phrase_list):  # Loop through terms in each phrase list
        #             # Loop for each term's positions in each document
        #             for j, term_occurrence in enumerate(self.term_to_doc_id_tf_scores[term][doc]['indexes']):
        #                 phrase_pos = self.term_to_doc_id_tf_scores[term][doc]['indexes'][j]
        #                 if i < len(phrase_list) - 1:  # Check if in bounds when looking at next term position
        #                     if phrase_pos + 1 not in self.term_to_doc_id_tf_scores[phrase_list[i + 1]][doc]['indexes']:
        #                         # Move on to the term's next position in doc if it is not the last in the array
        #                         if j != len(self.term_to_doc_id_tf_scores[term][doc]['indexes']) - 1:  # j is index pos
        #                             continue
        #                         phrase_in_doc = False  # Exit everything once one term fails
        #                         break
        #                     else:
        #                         break
        #             if phrase_in_doc is False:
        #                 break
        #         if phrase_in_doc is False:
        #             break
        #     if phrase_in_doc:
        #         valid_docs.add(doc)

        valid_docs = self.add_valid_docs(set_of_docs, phrase_dict)

        set_of_docs = valid_docs
        print(set_of_docs)

        for doc in set_of_docs:
            doc_id = doc
            score = self.combine_term_scores(processed_query, doc_id, len(set_of_docs))
            scores[doc_id] = score
        print(scores)
        return sorted(scores.keys(), key=scores.get, reverse=True)[:number_of_results]

    def add_valid_docs(self, set_of_docs, phrase_dict):
        valid_docs = set()

        for doc in set_of_docs:
            phrase_in_doc = self.check_all_phrases_in_doc(phrase_dict, doc)
            if phrase_in_doc:
                valid_docs.add(doc)

        return valid_docs

    def check_all_phrases_in_doc(self, phrase_dict, doc):
        for phrase_list in phrase_dict.values():  # Loop if there are multiple separate phrases in query
            phrase_in_doc = self.check_all_terms_in_phrase(phrase_list, doc)

            if phrase_in_doc is False: # Any phrase in query fails, doc is invalid
                return False
        
        return True

    def check_all_terms_in_phrase(self, phrase_list, doc):
        for i, term in enumerate(phrase_list):  # Loop through terms in each phrase list
            phrase_in_doc = self.check_term_in_doc(phrase_list, i, term, doc)

            if phrase_in_doc is False: # Any term in phrase fails, doc is invalid
                return False

        return True 

    def check_term_in_doc(self, phrase_list, i, term, doc):
        for j, _ in enumerate(self.term_to_doc_id_tf_scores[term][doc]['indexes']):
            phrase_pos = self.term_to_doc_id_tf_scores[term][doc]['indexes'][j]

            if i < len(phrase_list) - 1:  # Check if in bounds when looking at next term position
                phrase_in_doc, continue_loop = self.check_next_term(phrase_pos, phrase_list, i, j, term, doc)

                if continue_loop: # Continue looking in next position of the term
                    continue
                
                return phrase_in_doc # Doc is not valid if end reached or valid if next term in phrase was found
        
        return True # Every term in phrase was found
        
    def check_next_term(self, phrase_pos, phrase_list, i, j, term, doc):
        # Phrases must be listed sequentially: check next position for next term in phrase for match
        if phrase_pos + 1 not in self.term_to_doc_id_tf_scores[phrase_list[i + 1]][doc]['indexes']:
            # Move onto the term's next position in doc if it is not the last in the array
            if j != len(self.term_to_doc_id_tf_scores[term][doc]['indexes']) - 1:  # j is index pos
                return True, True # Next term was not found but not end of doc, continue

            return False, False # Next term was not found and end of doc, exit

        return True, False # Next term in phrase was found

    # Unused
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
