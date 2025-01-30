import requests
import json

url = 'https://hooks.slack.com/services/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'

payload = {
    "text": "Hello, World!"
}

response = requests.post(url, json=payload)

print(response.status_code)
