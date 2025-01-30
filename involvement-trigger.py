import requests
import json

url = 'https://hooks.slack.com/services/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'
payload = {
    "text": "Hello, Slack!"
}

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
print(response.status_code)
