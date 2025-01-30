import requests
import json

url = 'https://hooks.slack.com/services/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'

payload = {
    "channel": "#trigger-from-notion-to-slack",
    "username": "webhookbot",
    "text": "This is posted to #trigger-from-notion-to-slack and comes from a bot named webhookbot.",
    "icon_emoji": ":ghost:"
}

response = requests.post(url, json=payload)

print(response.text)
print(response.status_code)
