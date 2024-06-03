from langchain_community.retrievers import BM25Retriever
import json
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import re

def extract_api(text):
    match = re.search(r'\\n###Output: (.*)', text)

    # If a match is found, extract the matched text
    if match:
        return match.group(1).strip()
    else:
        return "No match found."

with open('/content/translated_api.jsonl', 'r') as f:
    data = [line for line in f]

docs = [Document(page_content=json.dumps(item, ensure_ascii= False)) for item in data]

texts = [doc.page_content for doc in docs]

tokenized_texts = [text.split() for text in texts]

bm25 = BM25Okapi(tokenized_texts)


query = "اريد تطبيق لتصنيف صور الحيوانات "
tokenized_query = query.split()

top_n = 5
top_docs_indices = bm25.get_top_n(tokenized_query, range(len(tokenized_texts)), n=top_n)
retriever_result = [docs[i].page_content for i in top_docs_indices]

for idx, result in enumerate(retriever_result):
    print(f"Result {idx+1}: {result}\n")

# Incorporate the result into a prompt for Ara-Gorilla
retriever_result_content = "".join(retriever_result[0])
retriever_result_content = extract_api(retriever_result_content)

question =  query + "Use this Reference API: " + retriever_result_content
print(question)