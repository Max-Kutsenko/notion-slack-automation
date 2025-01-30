from requests import post
from os import environ
from dotenv import load_dotenv

load_dotenv()

url = environ['INCOMING_WEBHOOK_URL']

payload = {
    "text": "Hello, World!"
}

response = post(url, json=payload)

print(response.status_code)
