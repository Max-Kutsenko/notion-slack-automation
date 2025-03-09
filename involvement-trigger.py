from requests import post, get
from os import environ
from dotenv import load_dotenv


def get_database_records(notion_api_key, database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    response = post(url, headers=headers, json={})

    return response.json()["results"]


def send_report_to_slack(incoming_webhook_url: str, employees: list):
    involvement_levels = {i: [] for i in range(0, 101, 5)}

    for employee in employees:
        involvement = employee["involvement"]
        involvement_levels.setdefault(involvement, []).append(employee)

    color_mapping = {
        0: "🔴",
        5: "🔴",
        10: "🟠",
        15: "🟠",
        20: "🟡",
        25: "🟡",
        30: "🟢",
        35: "🟢",
        40: "🔵",
        45: "🔵",
        50: "🟣",
        55: "🟣",
        60: "⚫",
        65: "⚫",
        70: "⚫",
        75: "⚫",
        80: "⚫",
        85: "⚫",
        90: "⚫",
        95: "⚫",
        100: "⚪",
    }

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Involvement Report*\n",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Involvements colors:*\n"
                "🔴 Red: 0%\n"
                "🟠 Orange: 10-15%\n"
                "🟡 Yellow: 20-25%\n"
                "🟢 Green: 30-35%\n"
                "🔵 Blue: 40-45%\n"
                "🟣 Purple: 50-55%\n"
                "⚫ Black: 60% and above\n"
                "⚪ White: 100%\n",
            },
        },
        {"type": "divider"},
    ]

    for involvement, emp_list in involvement_levels.items():
        if emp_list:
            color_icon = color_mapping.get(involvement, "⚪")
            employee_names = ", ".join(
                [
                    f"{emp['name'].strip().title()} ({emp['position']})"
                    for emp in emp_list
                ]
            )
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{color_icon} *{involvement}% Involvement:* {employee_names}",
                    },
                }
            )

    blocks.append({"type": "divider"})
    blocks.append(
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "The report will be posted every day at midnight (UTC)."},
        }
    )

    payload = {"text": "Involvement Report", "blocks": blocks}
    response = post(incoming_webhook_url, json=payload)

    return response.status_code


if __name__ == "__main__":
    load_dotenv()

    NOTION_API_KEY = environ["NOTION_API_KEY"]
    DATABASE_ID = environ["DATABASE_ID"]
    INCOMING_WEBHOOK_URL = environ["INCOMING_WEBHOOK_URL"]

    records = get_database_records(NOTION_API_KEY, DATABASE_ID)

    report_data = list()

    for record in records:
        actual_involvement = record["properties"]["Actual Involvement"]["rollup"][
            "number"
        ]

        employee_name = record["properties"][""]["title"][0]["plain_text"]
        employee_position = record["properties"]["Position"]["multi_select"][0][
            "name"
        ]
        employee_url = record["url"]

        employee_data = {
            "name": employee_name,
            "position": employee_position,
            "involvement": actual_involvement,
            "url": employee_url,
        }

        report_data.append(employee_data)

    status_code = send_report_to_slack(INCOMING_WEBHOOK_URL, report_data)
    print(status_code)
