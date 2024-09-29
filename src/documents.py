import json
import typing


class Document(typing.NamedTuple):
    doc_id: str
    text: str


class TransformedDocument(typing.NamedTuple):
    doc_id: str
    terms: list[str]


class DocumentStore:
    def add_document(self, doc: Document):
        pass

    def get_doc_by_id(self, doc_id: str) -> typing.Optional[Document]:
        pass

    def list_all(self) -> list[Document]:
        pass

    def write(self, path: str):
        pass


class ListDocumentStore(DocumentStore):
    def __init__(self, docs: typing.Optional[list[Document]]):
        if docs is None:
            self.docs = []
        else:
            self.docs = docs

    def add_document(self, doc: Document):
        self.docs.append(doc)

    # typing.Optional[Document] is the same as Document | None
    def get_doc_by_id(self, doc_id: str) -> typing.Optional[Document]:
        for d in self.docs:
            if d.doc_id == doc_id:
                return d
        return None

    def list_all(self) -> list[Document]:
        return self.docs

    def write(self, path: str):
        with open(path, 'w') as fp:
            for doc in self.docs:
                fp.write(json.dumps(doc._as_dict()) + '\n')

    @staticmethod
    def read(path: str) -> 'ListDocumentStore':
        docs = []
        with open(path, 'r') as fp:
            for line in fp:
                record = json.loads(line)
                docs.append(Document(doc_id=record['doc_id'], text=record['text']))
        return ListDocumentStore(docs)
        # return ListDocumentStore([
        #     Document(**json.loads(line)) for line in fp
        # ])


class DictDocumentStore(DocumentStore):
    def __init__(self, docs: typing.Optional[dict]):
        if docs is None:
            self.docs = dict()
        else:
            self.docs = docs

    def add_document(self, doc: Document):
        self.docs[doc.doc_id] = doc

    def get_doc_by_id(self, doc_id: str) -> typing.Optional[Document]:
        return self.docs.get(doc_id)

    def list_all(self) -> list[Document]:
        return list(self.docs.values())

    def write(self, path: str):
        with open(path, 'w') as fp:
            for doc in self.docs.keys():
                fp.write(json.dumps(doc._as_dict()) + '\n')

    @staticmethod
    def read(path: str) -> 'DictDocumentStore':
        docs = dict()
        with open(path, 'r') as fp:
            for line in fp:
                record = json.loads(line)
                docs[record['doc_id']] = Document(doc_id=record['doc_id'], text=record['text'])
                # docs.append(Document(doc_id=record['doc_id'], text=record['text']))
        return DictDocumentStore(docs)
