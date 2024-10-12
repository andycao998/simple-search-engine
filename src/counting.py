from collections import Counter
from documents import TransformedDocument

def count_tokens(tokens: list[str]) -> dict[str, int]:
    return Counter(tokens)

def count_tokens_in_doc(doc: TransformedDocument) -> Counter:
    return Counter(doc.terms)

def count_tokens_in_doc_collection(docs: list[TransformedDocument]) -> Counter:
    count = Counter()
    for doc in docs:
        count.update(doc.terms)
    return count

def num_documents_by_token(docs: list[TransformedDocument]) -> Counter:
    count = Counter()
    for doc in docs:
        count.update(set(doc.terms))
    return count
