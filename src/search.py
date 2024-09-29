
def match(document: str, query: str) -> bool:
    return query in document


def boolean_term_match(document: str, query: str) -> bool:
    query_terms = set(query.lower().split())
    document_terms = set(document.lower().split())
    return query_terms.issubset(document_terms)
    # for term in query_terms:
    #    if term not in document_terms:
    #        return False
    # return True


def search(documents: list[str], query: str) -> list[str]:
    # return [doc for doc in documents if match(doc, query)]
    output = []
    for doc in documents:
        if boolean_term_match(doc, query):
            output.append(doc)
    return output
