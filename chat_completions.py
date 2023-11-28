# THIS IS USING CHAT COMPLETIONS
import requests
import json
import sseclient

API_KEY = ''


def request_with_streaming(prompt):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Accept': 'text/event-stream',
        'Authorization': f'Bearer {API_KEY}'
    }
    body = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 100,
        "temperature": 0,
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "assistant",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, stream=True, headers=headers, json=body)
        client = sseclient.SSEClient(response)
        for event in client.events():
            if event.data.strip() == 'data: [DONE]':
                break

            try:
                if not event.data.strip().endswith('[DONE]'):
                    data = json.loads(event.data.replace('data: ', ''))
                    delta = data['choices'][0]['delta']
                    content = delta.get('content', '')
                    print(content, end="", flush=True)
            except json.JSONDecodeError as json_err:
                print(f"JSON parsing error: {json_err}")
            except Exception as e:
                print(f"An error occurred while processing the event: {e}")
    except Exception as e:
        print(f"An error occurred during the request: {e}")


if __name__ == '__main__':
    user_prompt = input("Enter a prompt: ")
    request_with_streaming(user_prompt)
