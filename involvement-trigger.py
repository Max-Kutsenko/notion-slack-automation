import requests
import json

url = 'https://hooks.slack.com/services/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'

payload = {
    "channel": "#trigger-from-notion-to-slack",
    "username": "webhookbot",
    "text": "This is posted to #trigger-from-notion-to-slack and comes from a bot named webhookbot.",
    "icon_emoji": ":ghost:"
}

response = requests.post(url, data=json.dumps({"payload": json.dumps(payload)}), headers={'Content-Type': 'application/json'})

print(response)
print(response.status_code)