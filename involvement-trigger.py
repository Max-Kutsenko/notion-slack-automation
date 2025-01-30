import requests
import json

url = 'https://hooks.slack.com/services/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'

payload = {
    "text": "Hello, World!"
}

response = requests.post(url, json=payload)

print(response.status_code)