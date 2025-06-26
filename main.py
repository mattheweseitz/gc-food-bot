import os
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import requests

# Configuration
GOOGLE_CREDS_ENV_VAR = "GOOGLE_CREDS_BASE64"
GOOGLE_SHEET_NAME = "GC-Schedule"
GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")
# GROUPME_BOT_ID = "dea34be60fd4efa15e551ec965" # Use this Bot ID to test the script
MESSAGE = (
    "This is your friendly Forest Ridge Bot asking you to please give a thumbs "
    "up if you're coming this week and post below if you can bring anything!\n\n"
)

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_google_credentials():
    b64_creds = os.environ.get(GOOGLE_CREDS_ENV_VAR)
    if not b64_creds:
        raise ValueError("Environment variable GOOGLE_CREDS_BASE64 is missing.")
    
    try:
        creds_json = base64.b64decode(b64_creds).decode("utf-8")
        creds_dict = json.loads(creds_json)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
        print("Successfully loaded Google credentials from environment.")
        return credentials
    except Exception as e:
        raise ValueError(f"Failed to load Google credentials: {e}")

def get_this_weeks_study():
    try:
        credentials = get_google_credentials()
        gc = gspread.authorize(credentials)
        print("Successfully authenticated with Google Sheets.")
    except Exception as e:
        print(f"ERROR: Google Sheets authentication failed - {e}")
        return None

    try:
        sheet = gc.open(GOOGLE_SHEET_NAME).sheet1
        data = sheet.get_all_records()
        print(f"Fetched {len(data)} rows from sheet '{GOOGLE_SHEET_NAME}'.")
    except Exception as e:
        print(f"ERROR: Failed to open or read sheet - {e}")
        return None

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday

    for row in data:
        try:
            study_date = datetime.strptime(row['Date'], "%m/%d/%Y").date()
            if start_of_week <= study_date <= end_of_week:
                print(f"Found study scheduled for this week: {row}")
                return row
        except Exception as e:
            print(f"WARNING: Failed to parse date in row {row} - {e}")

    print("No Bible study scheduled for this week.")
    return None

def send_groupme_message(message):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {
        "bot_id": GROUPME_BOT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 202:
            print("Message sent to GroupMe successfully.")
        else:
            print(f"ERROR: GroupMe message failed - {response.status_code}, {response.text}")
    except Exception as e:
        print(f"ERROR: Exception while sending GroupMe message - {e}")

def main():
    print("Starting Bible Study Notifier...")

    # Only proceed if today is Monday
    if datetime.today().weekday() != 0:
        print("Today is not Monday. Exiting without sending message.")
        return

    details = get_this_weeks_study()
    if not details:
        print("No details found for this week. Exiting.")
        return

    msg = MESSAGE + (
        f"📅 Study is on *{details['Night']}* ({details['Date']})\n"
        f"🍽 Dinner: {details['Dinner']}\n"
        f"📜 Passage: {details['Passage']}\n\n"
        f"Let us know if you're coming!"
    )

    send_groupme_message(msg)

if __name__ == "__main__":
    main()
