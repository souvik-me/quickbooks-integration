import json
from invoice_creator import process_invoice

def main():
    with open("sample_order.json") as f:
        order = json.load(f)

    process_invoice(order)

if __name__ == "__main__":
    main()
