from typing import Any, List, Dict
import openai
import requests
from secrets import DATABASE_INTERFACE_BEARER_TOKEN
import logging

def query_database(query_prompt: str) -> Dict[str, Any]:
    url = "http://0.0.0.0:8000/query"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {DATABASE_INTERFACE_BEARER_TOKEN}",
    }
    data = {"queries": [{"query": query_prompt, "top_k": 5}]}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise ValueError(f"Error: {response.status_code} : {response.content}")


def apply_prompt_template(question: str) -> str:
    prompt = f"""
        By considering above input from me, answer the question: {question}
    """
    return prompt

def call_chatgpt_api(user_question: str, chunks: List[str]) -> Dict[str, Any]:
    messages = list(
        map(lambda chunk: {
            "role": "user",
            "content": chunk
        }, chunks))
    question = apply_prompt_template(user_question)
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )
    return response


def ask(user_question: str) -> Dict[str, Any]:
    chunks_response = query_database(user_question)
    chunks = []
    for result in chunks_response["results"]:
        for inner_result in result["results"]:
            chunks.append(inner_result["text"])
    
    logging.info("User's questions: %s", user_question)
    logging.info("Retrieved chunks: %s", chunks)
    
    response = call_chatgpt_api(user_question, chunks)
    logging.info("Response: %s", response)
    
    return response["choices"][0]["message"]["content"]