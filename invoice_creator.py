from quickbooks_api import get_or_create_customer, get_or_create_item, create_invoice

def process_invoice(order_data):
    print("🔄 Processing customer...")
    customer = get_or_create_customer(order_data["customer"])

    print("🔄 Processing items...")
    line_items = []

    for item in order_data["items"]:
        qbo_item = get_or_create_item(item)

        line = {
            "DetailType": "SalesItemLineDetail",
            "Amount": round(item["unit_price"] * item["quantity"], 2),
            "SalesItemLineDetail": {
                "ItemRef": {
                    "value": qbo_item["Id"],
                    "name": qbo_item["Name"]
                },
                "Qty": item["quantity"],
                "UnitPrice": item["unit_price"]
                # TaxCodeRef removed
            }
        }
        line_items.append(line)

    print("🧾 Creating invoice...")
    invoice = create_invoice(customer, line_items)
    print("✅ Invoice creation complete.")
    return invoice
