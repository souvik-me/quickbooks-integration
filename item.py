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

def find_item_by_sku(sku):
    tokens = get_tokens()
    access_token = tokens["access_token"]

    query = f"select * from Item where SKU = '{sku}'"
    url = f"{BASE_URL}/v3/company/{REALM_ID}/query?query={query}&minorversion=65"

    res = requests.get(url, headers=get_headers(access_token))
    data = res.json()

    if res.status_code == 200 and data.get("QueryResponse", {}).get("Item"):
        return data["QueryResponse"]["Item"][0]

    return None

def create_item(name, sku, rate):
    tokens = get_tokens()
    access_token = tokens["access_token"]

    url = f"{BASE_URL}/v3/company/{REALM_ID}/item?minorversion=65"

    item_payload = {
        "Name": name,
        "Sku": sku,
        "UnitPrice": rate,
        "Type": "NonInventory",
        "IncomeAccountRef": {
            "value": "79"
        }
    }

    res = requests.post(url, headers=get_headers(access_token), json=item_payload)
    return res.json()

def get_or_create_item(sku, name, rate):
    existing_item = find_item_by_sku(sku)
    if existing_item:
        print(f"Item found: {name}")
        return existing_item["Id"]

    print(f"Creating item: {name}")
    new_item = create_item(name, sku, rate)
    return new_item.get("Item", {}).get("Id")

if __name__ == "__main__":
    sku = input("Enter SKU: ")
    name = input("Enter Item Name: ")
    rate = float(input("Enter Item Rate: "))

    item_id = get_or_create_item(sku, name, rate)
    print("QuickBooks Item ID:", item_id)
