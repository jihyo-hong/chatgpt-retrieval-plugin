import os
import flask
import openai
from flask import Flask, request, render_template
import requests
import logging

openai.api_key = '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'
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html');

@app.route('/completion', methods=['POST'])
def completion_api():
    q = request.get_json().get('prompt')

    # 검색 플러그인 테스트용 코드(오류)
    """
    DATABASE_INTERFACE_BEAR_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.bIgxJr16K-WjXHHQ-Ev9sfrMHGePIR3r67nMgVwgrBk"
  
    # db에 쿼리 보내기
    url = "http://0.0.0.0:8000/query"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {DATABASE_INTERFACE_BEAR_TOKEN}",
    }
    data = {"queries": [{"query": q, "top_k": 5}]}

    response = requests.post(url, json=data, headers=headers)
    chunk_response = response.json()
    chunks = []

    for result in chunk_response["results"]:
        for inner_result in result["results"]:
            chunks.append(inner_result["text"])

    logging.info("User's questions: %s", q)
    logging.info("Retrieved chunks: %s", chunks)

    # api 호출
    messages = list(
        map(lambda chunk: {
            "role": "user",
            "content": chunk
        }, chunks))
    messages.append({"role": "user", "content": q})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7,  # High temperature leads to a more creative response.
    )

    """
    def stream():
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', 
            messages=[{"role": "user", "content": q}],
            stream=True)
        for line in completion:
            chunk = line['choices'][0].get('delta', {}).get('content', '')
            if chunk:
                yield chunk
    return flask.Response(stream(), mimetype='text/event-stream')

