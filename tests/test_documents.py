from unittest import TestCase
from documents import Document, DictDocumentStore


class TestDictDocumentStore(TestCase):
    def test_add_and_get_doc_by_id(self):
        doc_store = DictDocumentStore()
        doc = Document(doc_id='1', text='text1')
        doc_store.add_document(doc)
        self.assertEqual(doc, doc_store.get_doc_by_id('1'))
        self.assertIsNone(doc_store.get_doc_by_id('2'))

    def test_list_all(self):
        doc_store = DictDocumentStore()
        doc1 = Document(doc_id='1', text='text1')
        doc2 = Document(doc_id='2', text='text2')
        doc_store.add_document(doc1)
        doc_store.add_document(doc2)
        self.assertEqual([doc1, doc2], doc_store.list_all())
