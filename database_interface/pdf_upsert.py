from typing import Any, Dict
import requests
import os
from secrets import DATABASE_INTERFACE_BEARER_TOKEN
from PyPDF2 import PdfReader

SEARCH_TOP_K = 3 # 사용자의 질문으로부터 검색할 청크의 개수


def upsert_file(directory: str):
    """
    Upload all files under a directory to the vector database.
    """
    url = "http://0.0.0.0:8000/upsert-file"
    headers = {"Authorization": "Bearer " + DATABASE_INTERFACE_BEARER_TOKEN}
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_path = directory + "/" + filename
            reader = PdfReader(file_path)
            pages = reader.pages
            text = ""
            for page in pages:
                sub = page.extract_text()
                text += sub
            files.append(("file", (filename, text, "text/plain")))
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                print(filename + " uploaded successfully.")
            else:
                print(f"Error: {response.status_code} {response.content} for uploading " + filename)


def upsert(id: str, content: str):
    """
    Upload one piece of text to the database.
    """
    url = "http://0.0.0.0:8000/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + DATABASE_INTERFACE_BEARER_TOKEN,
    }

    data = {
        "documents": [{
            "id": id,
            "text": content,
        }]
    }
    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        print("uploaded successfully.")
    else:
        print(f"Error: {response.status_code} {response.content}")


def query_database(query_prompt: str) -> Dict[str, Any]:
    """
    Query vector database to retrieve chunk with user's input question.
    """
    url = "http://0.0.0.0:8000/query"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {DATABASE_INTERFACE_BEARER_TOKEN}",
    }
    data = {"queries": [{"query": query_prompt, "top_k": SEARCH_TOP_K}]}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        # process the result
        return result
    else:
        raise ValueError(f"Error: {response.status_code} : {response.content}")


if __name__ == "__main__":
    upsert_file("/home/jihyo/chatgpt-retrieval-plugin/test/drtrue")
    