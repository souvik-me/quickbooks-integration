import requests
import base64
import os
from dotenv import load_dotenv
from mongodb import save_tokens

load_dotenv()

client_id = os.getenv("QBO_CLIENT_ID")
client_secret = os.getenv("QBO_CLIENT_SECRET")
redirect_uri = os.getenv("QBO_REDIRECT_URI")

def get_access_token(auth_code):
    url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print("✅ Access token retrieved successfully.")
        return response.json()
    else:
        print("❌ Failed to retrieve access token.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return {}

if __name__ == "__main__":
    auth_code = input("🔑 Enter the authorization code from Postman redirect URL: ")
    tokens = get_access_token(auth_code)
    if "access_token" in tokens:
        save_tokens(tokens)
        print("✅ Tokens saved to MongoDB.")
    else:
        print("❌ Token was not saved.")
