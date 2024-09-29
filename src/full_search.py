import os
from indexing_process import indexing_process
from query_process import QueryProcess
import timeit


def run_search_tf_idf_inverted():
    doc_store = None
    index = None
    query = input('Please enter your query: ')
    while query:
        if doc_store is None and index is None:
            doc_store, index = indexing_process(os.path.abspath('../resources/msmarco_passage_dev_rel_docs.json'),
                                                'Tf_Idf_Inverted')
        query_class = QueryProcess(document_store=doc_store, index=index,
                                   stopword_list_path=os.path.abspath('../resources/stopword.json'),
                                   use_stopword=False)
        time_results = input('Time results? (True or False): ')
        if time_results == 'True':
            print(timeit.timeit(lambda: query_class.search(query='credit card', number_of_results=10), number=100))
        else:
            print(query_class.search(query=query, number_of_results=10))
        query = input('Please enter your query: ')


def run_search_tf_idf_inverted_stopword():
    doc_store = None
    index = None
    query = input('Please enter your query: ')
    while query:
        if doc_store is None and index is None:
            doc_store, index = indexing_process(os.path.abspath('../resources/msmarco_passage_dev_rel_docs.json'),
                                                'Tf_Idf_Inverted')
        query_class = QueryProcess(document_store=doc_store, index=index,
                                   stopword_list_path=os.path.abspath('../resources/stopword.json'),
                                   use_stopword=True)
        time_results = input('Time results? (True or False): ')
        if time_results == 'True':
            print(timeit.timeit(lambda: query_class.search(query='credit card', number_of_results=10), number=100))
        else:
            print(query_class.search(query=query, number_of_results=10))
        query = input('Please enter your query: ')


def run_search_tf_idf_inverted_phrase():
    doc_store = None
    index = None
    query = input('Please enter your query: ')
    while query:
        if doc_store is None and index is None:
            doc_store, index = indexing_process(os.path.abspath('../resources/msmarco_passage_dev_rel_docs.json'),
                                                'Tf_Idf_Inverted_Phrase')
        query_class = QueryProcess(document_store=doc_store, index=index,
                                   stopword_list_path=os.path.abspath('../resources/stopword.json'),
                                   use_stopword=False)
        time_results = False  # input('Time results? (True or False): ')
        if time_results == 'True':
            print(timeit.timeit(lambda: query_class.search(query=query, number_of_results=10), number=100))
        else:
            print(query_class.search(query=query, number_of_results=10))
        query = input('Please enter your query: ')


def run_search_tf_idf():
    doc_store = None
    index = None
    query = input('Please enter your query: ')
    while query:
        if doc_store is None and index is None:
            doc_store, index = indexing_process(os.path.abspath('../resources/msmarco_passage_dev_rel_docs.json'),
                                                'Tf_Idf')
        query_class = QueryProcess(document_store=doc_store, index=index,
                                   stopword_list_path=os.path.abspath('../resources/stopword.json'),
                                   use_stopword=False)
        time_results = input('Time results? (True or False): ')
        if time_results == 'True':
            print(timeit.timeit(lambda: query_class.search(query='credit card', number_of_results=10), number=100))
        else:
            print(query_class.search(query=query, number_of_results=10))
        query = input('Please enter your query: ')
