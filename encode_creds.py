# NOTE: This script should only be needed on Windows machines to
# encode the google creds to base64
# Mac/UNIX systems have a built in base64 command in the terminal.

import base64

with open("google-creds.json", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

with open("google-creds.b64", "w") as out:
    out.write(encoded)

print("✅ google-creds.b64 created successfully.")
