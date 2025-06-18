import requests
import os

BOT_ID = os.getenv("GROUPME_BOT_ID")

MESSAGE = "This is your friendly Forest Ridge Bot asking you to please give a thumbs up if you're coming this week and post below if you can bring anything!"

def send_message():
    if not BOT_ID:
        print("Error: GROUPME_BOT_ID not set.")
        return

    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": BOT_ID,
        "text": MESSAGE
    }

    response = requests.post(url, json=data)

    if response.status_code == 202:
        print("Message sent successfully!")
    else:
        print(f"Error sending message: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_message()
