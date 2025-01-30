import requests
import json

url = 'https://hooks.slack.com/services/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'
payload = {
    "text": "Hello, Slack!"
}

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
print(response)
print(response.status_code)
