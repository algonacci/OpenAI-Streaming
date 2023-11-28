# THIS IS USING COMPLETIONS (LEGACY)
import requests
import json
from sseclient import SSEClient

API_KEY = ''


def perform_request_with_streaming(prompt):
    req_url = 'https://api.openai.com/v1/completions'
    req_headers = {
        'Accept': 'text/event-stream',
        'Authorization': f'Bearer {API_KEY}'
    }
    req_body = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0,
        "stream": True,
    }
    response = requests.post(req_url,
                             stream=True,
                             headers=req_headers,
                             json=req_body)
    client = SSEClient(response)
    for event in client.events():
        if event.data != '[DONE]':
            print(json.loads(event.data)['choices']
                  [0]['text'], end="", flush=True)


if __name__ == '__main__':
    user_prompt = input("Enter a prompt: ")
    perform_request_with_streaming(user_prompt)
