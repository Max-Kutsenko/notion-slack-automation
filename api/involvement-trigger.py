from datetime import datetime
import json

def handler(request):
    print(f"I'm working... {datetime.now()}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Job executed"}),
    }
