import os
import requests
from dotenv import load_dotenv
from mongodb import get_tokens

load_dotenv()

REALM_ID = os.getenv("QBO_REALM_ID")
BASE_URL = "https://sandbox-quickbooks.api.intuit.com"


def get_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def find_customer_by_email(email):
    tokens = get_tokens()
    access_token = tokens["access_token"]

    query = f"select * from Customer where PrimaryEmailAddr = '{email}'"
    url = f"{BASE_URL}/v3/company/{REALM_ID}/query?query={query}&minorversion=65"

    res = requests.get(url, headers=get_headers(access_token))
    data = res.json()

    if res.status_code == 200 and data.get("QueryResponse", {}).get("Customer"):
        return data["QueryResponse"]["Customer"][0]

    return None


def create_customer(email, first_name, last_name):
    tokens = get_tokens()
    access_token = tokens["access_token"]

    url = f"{BASE_URL}/v3/company/{REALM_ID}/customer?minorversion=65"

    payload = {
        "GivenName": first_name,
        "FamilyName": last_name,
        "PrimaryEmailAddr": {
            "Address": email
        }
    }

    res = requests.post(url, headers=get_headers(access_token), json=payload)
    return res.json()


def get_or_create_customer(email, first_name, last_name):
    existing_customer = find_customer_by_email(email)
    if existing_customer:
        print("✅ Customer found in QuickBooks.")
        return existing_customer["Id"]

    print("➕ Customer not found. Creating...")
    new_customer = create_customer(email, first_name, last_name)
    return new_customer.get("Customer", {}).get("Id")


# 👉 For manual testing
if __name__ == "__main__":
    email = input("📧 Enter customer email: ")
    first_name = input("🧍 First Name: ")
    last_name = input("🧍‍♂️ Last Name: ")

    customer_id = get_or_create_customer(email, first_name, last_name)
    print("🔁 QuickBooks Customer ID:", customer_id)
