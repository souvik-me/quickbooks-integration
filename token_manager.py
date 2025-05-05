import requests, base64, os
from dotenv import load_dotenv
from mongodb import load_tokens, save_tokens

load_dotenv()

client_id = os.getenv("QBO_CLIENT_ID")
client_secret = os.getenv("QBO_CLIENT_SECRET")


def get_valid_access_token():
    tokens = load_tokens()
    if not tokens:
        raise Exception("No tokens found. Please run oauth.py first.")

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if is_token_expired(tokens):  # you can enhance with expiry check
        print("🔁 Refreshing access token...")
        return refresh_access_token(refresh_token)

    return access_token


def refresh_access_token(refresh_token):
    token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, headers=headers, data=payload)

    if response.status_code == 200:
        new_tokens = response.json()
        new_tokens["refresh_token"] = new_tokens.get("refresh_token", refresh_token)
        save_tokens(new_tokens)
        return new_tokens["access_token"]
    else:
        raise Exception(f"Failed to refresh token: {response.text}")


def is_token_expired(tokens):
   
    return False 
