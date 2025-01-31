from requests import post, get
from os import environ
from dotenv import load_dotenv


def get_database_records(notion_api_key, database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = post(url, headers=headers, json={})

    return response.json()

def send_report_to_slack(incoming_webhook_url: str, smaller_involvement_employees: dict):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Involvement Report*\nHere are the involvement levels of employees:"
            }
        },
        {
            "type": "divider"
        }
    ]

    for url, involvement in smaller_involvement_employees.items():
        employee_name = url.split('/')[-1].replace('-', ' ').title()
        involvement_text = f"*Involvement:* {involvement}" if involvement > 0 else "*Involvement:* None"
        
        blocks.append({
            "type": "section",
            "block_id": f"section_{employee_name.replace(' ', '_')}",
            "text": {
                "type": "mrkdwn",
                "text": f"<{url}|{employee_name}> \n{involvement_text}"
            }
        })

    blocks.append({
        "type": "divider"
    })
    
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "The report will be posted every day)"
        }
    })

    payload = {
        "text": "Involvement Report",
        "blocks": blocks
    }

    response = post(incoming_webhook_url, json=payload)

    return response.status_code

if __name__ == "__main__":
    load_dotenv()

    NOTION_API_KEY = environ['NOTION_API_KEY']
    DATABASE_ID = environ['DATABASE_ID']
    INCOMING_WEBHOOK_URL = environ['INCOMING_WEBHOOK_URL']

    records = get_database_records(NOTION_API_KEY, DATABASE_ID)['results']

    smaller_involvement_employees = dict()

    for record in records:
        actual_involvement = record['properties']['Actual Involvement']['rollup']['number']
        if (actual_involvement < 100):
            smaller_involvement_employees[record['url']] = actual_involvement

    status_code = send_report_to_slack(INCOMING_WEBHOOK_URL, smaller_involvement_employees)
    print("Response Status Code:", status_code)
