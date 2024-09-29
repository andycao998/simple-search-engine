import json
from collections import defaultdict

from query_process import QueryProcess


def read_queries(path: str) -> dict[str, str]:
    """
    Read queries
    :param path:
    :return: Dictionary of query ids to query text
    """
    queries = dict()
    with open(path, 'r') as fp:
        for line in fp:
            record = json.loads(line)
            queries[record['query_id']] = record['text']
    return queries


def read_eval_data(queries_path: str, eval_data_path: str) -> dict[str, set[str]]:
    """
    Read evaluation data
    :param queries_path:
    :param eval_data_path:
    :return: Dictionary mapping a query to expected doc_ids


    Example:
    For eval data
    {"query_id": "1102432", "doc_id": "2026790", "relevance": 1, "iteration": "0"}
    {"query_id": "1102431", "doc_id": "7066866", "relevance": 1, "iteration": "0"}
    {"query_id": "1102431", "doc_id": "7066867", "relevance": 1, "iteration": "0"}
    and
    {"query_id": "1102432", "text": ". what is a corporation?"}
    {"query_id": "1102431", "text": "why did rachel carson write an obligation to endure"}
    the output will be
    {
        ". what is a corporation?": {"2026790"}}
        "why did rachel carson write an obligation to endure": {"7066866", "7066867"}
    }
    """
    queries = read_queries(queries_path)
    eval_data = defaultdict(set)
    with open(eval_data_path) as fp:
        for line in fp:
            record = json.loads(line)
            query_id = record['query_id']
            doc_id = record['doc_id']
            eval_data[queries[query_id]].add(doc_id)  # {'1102431': {2026790}}
    return eval_data


def evaluate(query_process: QueryProcess, eval_data: dict[str, set[str]]) -> float:
    score = 0
    for query, expected_doc_ids in eval_data.items():
        returned_doc_ids = query_process.search(query, 10)
        score += len(set(returned_doc_ids) & expected_doc_ids) / 10
    return score / len(eval_data)
