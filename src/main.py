import os
import full_search
import tkinter
from tkinter import scrolledtext
from documents import DocumentStore
from indexing_process import indexing_process
from index import BaseIndex

def perform_search(query: str, doc_store: DocumentStore, index: BaseIndex):
    results = full_search.run_search(query, doc_store, index)

    result_area.delete(1.0, tkinter.END)
    result_area.insert(tkinter.INSERT, results)

def index_docs():
    doc_store = None
    index = None
    # Default option of phrase-enabled searching [Tf_Idf, Tf_Idf_Inverted, Tf_Idf_Inverted_Phrase] <- swap with any
    doc_store, index = indexing_process(os.path.abspath('../resources/msmarco_passage_dev_rel_docs.json'), 'Tf_Idf_Inverted_Phrase')
    return doc_store, index

if __name__ == '__main__':
    doc_store, index = index_docs()

    root = tkinter.Tk()
    root.title("Search Engine")

    query_label = tkinter.Label(root, text="Enter your search query:")
    query_label.pack()

    query_entry = tkinter.Entry(root, width=50)
    query_entry.pack()

    search_button = tkinter.Button(root, text="Search", command=lambda: perform_search(query_entry.get(), doc_store, index))
    search_button.pack()

    result_area = scrolledtext.ScrolledText(root, width=120, height=40)
    result_area.pack()
    
    root.mainloop()

