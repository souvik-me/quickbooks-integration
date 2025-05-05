import os
import requests
from dotenv import load_dotenv
from mongodb import get_tokens

load_dotenv()

REALM_ID = os.getenv("QBO_REALM_ID")
BASE_URL = "https://sandbox-quickbooks.api.intuit.com"
MINOR_VERSION = "65"


def get_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def query_customer_by_email(email):
    """Search for a customer in QuickBooks using their email address."""
    tokens = get_tokens()
    access_token = tokens["access_token"]
    query = f"SELECT * FROM Customer WHERE PrimaryEmailAddr = '{email}'"
    url = f"{BASE_URL}/v3/company/{REALM_ID}/query?query={query}&minorversion={MINOR_VERSION}"

    response = requests.get(url, headers=get_headers(access_token))
    if response.status_code == 200:
        customers = response.json().get("QueryResponse", {}).get("Customer", [])
        return customers[0] if customers else None
    else:
        raise Exception(f"❌ Failed to query customer: {response.text}")


def create_customer(email, first_name, last_name):
    """Create a new customer in QuickBooks."""
    tokens = get_tokens()
    access_token = tokens["access_token"]
    url = f"{BASE_URL}/v3/company/{REALM_ID}/customer?minorversion={MINOR_VERSION}"

    payload = {
        "GivenName": first_name,
        "FamilyName": last_name,
        "PrimaryEmailAddr": {"Address": email}
    }

    response = requests.post(url, headers=get_headers(access_token), json=payload)
    if response.status_code in [200, 201]:
        return response.json()["Customer"]
    else:
        raise Exception(f"❌ Failed to create customer: {response.text}")


def get_or_create_customer(email, first_name, last_name):
    """Retrieve existing customer by email, or create one if not found."""
    customer = query_customer_by_email(email)
    if customer:
        print("✅ Customer found in QuickBooks.")
        return customer["Id"]

    print("➕ Customer not found. Creating...")
    new_customer = create_customer(email, first_name, last_name)
    print("✅ Customer created.")
    return new_customer.get("Id")


# Optional: Manual testing interface
if __name__ == "__main__":
    try:
        email = input("📧 Enter customer email: ").strip()
        first_name = input("🧍 First Name: ").strip()
        last_name = input("🧍‍♂️ Last Name: ").strip()

        customer_id = get_or_create_customer(email, first_name, last_name)
        print("🔁 QuickBooks Customer ID:", customer_id)
    except Exception as e:
        print(str(e))
