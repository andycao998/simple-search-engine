import json

import counting
from documents import Document, TransformedDocument, DictDocumentStore, DocumentStore
from index import BaseIndex
from tf_idf_index import TfIdfIndex
from tf_idf_inverted_index import TfIdfInvertedIndex
from tf_idf_inverted_index_phrase import TfIdfInvertedIndexPhrase
from tokenizer import tokenize

# For testing: unreachable
def text_acquisition() -> DocumentStore:
    doc_store = DictDocumentStore(None) # Currently using dictionary implementation [ListDocumentStore, DictDocumentStore] <- swap any
    doc_store.add_document(Document(doc_id='0', text='red is a color'))
    doc_store.add_document(Document(doc_id='1', text='red and blue'))
    return doc_store

def transform_documents(documents: list[Document]) -> list[TransformedDocument]:
    return [TransformedDocument(doc_id=doc.doc_id, terms=tokenize(doc.text)) for doc in documents] # Tokenize docs, removing '.,%$;'

def create_index(transformed_documents: list[TransformedDocument], method: str) -> BaseIndex:
    """
    Takes a list of TransformedDocument and creates an index out of them.
    :param transformed_documents: list of TransformedDocuments.
    :param method: string condition to switch from default index creation (TfIdfInvertedIndexPhrase) to TfIdfIndex or TfIdfInvertedIndex
    :return: Index
    """
    if method == 'Tf_Idf':
        index = TfIdfIndex()
    elif method == 'Tf_Idf_Inverted':
        index = TfIdfInvertedIndex()
    else:
        index = TfIdfInvertedIndexPhrase()

    for doc in transformed_documents:
        index.add_document(doc)
        index.index_term_positions(doc)
    return index

def docs_from_json(json_file_location: str) -> DocumentStore:
    doc_store = DictDocumentStore(None)

    with open(json_file_location, 'r') as fp:
        for line in fp:
            doc_store.add_document(Document(doc_id=json.loads(line)['doc_id'], text=json.loads(line)['text']))
    return doc_store

def compute_most_common_terms(json_file_location: str):
    documents = docs_from_json(json_file_location)
    transformed_documents = transform_documents(documents.list_all())
    common_terms = [t[0] for t in counting.count_tokens_in_doc_collection(transformed_documents).most_common(100)]
    return common_terms

def generate_stop_word_list(json_file_location: str):
    json_obj = json.dumps(compute_most_common_terms(json_file_location), indent=4)
    with open('stopword.json', 'w') as fp:
        fp.write(json_obj)

def indexing_process(json_file_location: str, method: str) -> tuple[DocumentStore, BaseIndex]:  # tuple[DictDocumentStore, Index]:
    documents = docs_from_json(json_file_location)
    transformed_documents = transform_documents(documents.list_all())
    index = create_index(transformed_documents, method)
    return documents, index
