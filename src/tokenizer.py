def tokenize(query_str):
    symbols = list('.,%$;')
    for s in symbols:
        query_str = query_str.replace(s, f' {s} ')
    return query_str.lower().split()
