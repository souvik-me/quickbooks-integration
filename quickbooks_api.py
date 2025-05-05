import os
import requests
from dotenv import load_dotenv
from token_manager import get_valid_access_token

load_dotenv()

QBO_REALM_ID = os.getenv("QBO_REALM_ID")
BASE_URL = os.getenv("QBO_BASE_URL")

HEADERS = lambda token: {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_or_create_customer(customer_data):
    token = get_valid_access_token()

    display_name = customer_data.get("DisplayName")
    email = customer_data.get("PrimaryEmailAddr", {}).get("Address")

    if not display_name:
        raise ValueError("Customer 'DisplayName' is required.")

    # Check if customer exists
    query = f"select * from Customer where DisplayName = '{display_name}'"
    url = f"{BASE_URL}/v3/company/{QBO_REALM_ID}/query?query={query.replace(' ', '%20')}"
    response = requests.get(url, headers=HEADERS(token))

    if response.status_code == 200:
        customers = response.json().get("QueryResponse", {}).get("Customer", [])
        if customers:
            return customers[0]

    # Create customer if not found
    payload = {
        "DisplayName": display_name,
    }

    if email:
        payload["PrimaryEmailAddr"] = {"Address": email}

    url = f"{BASE_URL}/v3/company/{QBO_REALM_ID}/customer"
    response = requests.post(url, headers=HEADERS(token), json=payload)

    if response.status_code in [200, 201]:
        return response.json()["Customer"]
    else:
        raise Exception(f"❌ Failed to create customer: {response.text}")

def get_or_create_item(item_data):
    token = get_valid_access_token()

    # Check if item exists
    query = f"select * from Item where Name = '{item_data['name']}'"
    url = f"{BASE_URL}/v3/company/{QBO_REALM_ID}/query?query={query.replace(' ', '%20')}"
    response = requests.get(url, headers=HEADERS(token))

    if response.status_code == 200:
        items = response.json().get("QueryResponse", {}).get("Item", [])
        if items:
            return items[0]

    # Create item if not found
    payload = {
        "Name": item_data["name"],
        "Description": item_data.get("description", item_data["name"]),
        "UnitPrice": item_data["unit_price"],
        "Type": "Service",
        "IncomeAccountRef": {
            "value": "79"
        }
    }

    url = f"{BASE_URL}/v3/company/{QBO_REALM_ID}/item"
    response = requests.post(url, headers=HEADERS(token), json=payload)

    if response.status_code in [200, 201]:
        return response.json()["Item"]
    else:
        raise Exception(f"❌ Failed to create item: {response.text}")

def create_invoice(customer, line_items):
    token = get_valid_access_token()

    payload = {
        "CustomerRef": {
            "value": customer["Id"]
        },
        "Line": line_items
    }

    url = f"{BASE_URL}/v3/company/{QBO_REALM_ID}/invoice"
    response = requests.post(url, headers=HEADERS(token), json=payload)

    if response.status_code in [200, 201]:
        invoice = response.json()["Invoice"]
        print(f"✅ Invoice created with ID: {invoice['Id']}")
        return invoice
    else:
        raise Exception(f"❌ Failed to create invoice: {response.text}")
