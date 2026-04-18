import json
from datetime import datetime

file_name = "market_file.json"

def load_items():
    with open(file_name, "r") as file:
        return json.load(file)
    
def save_item(items):
    with open(file_name, "w") as file:
        json.dump(items, file, indent=4)

def show_items(items):
    if len(items) == 0:
        print("No products available.")
    else:
        print("\n---Products available to buy---")
        for i in items:
            print(f"{i["id"]}- {i["name"]} | Price: {i["price"]} | Stock: {i["stock"]}")


def add_item(items):
    name = input("Write the product name: ").strip()
    price = float(input("Write the product price: ").strip())
    stock = int(input("Write the product stock: ").strip())
    id_product = max([i["id"] for i in items], default=0) + 1
    # to add the product information to the json file
    items.append({"id": id_product, "name": name, "price": price, "stock": stock})
    save_item(items)
    print("Product saved successfully.")

def buy_item(items):
    pass

def main():
    items = load_items()

    while True:
        print("\n---Market options---")
        print("1. View products")
        print("2. Add product")
        print("3. Buy product")
        print("4. Leave")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_items(items)
        elif choice == "2":
            add_item(items)
        elif choice == "3":
            buy_item(items)
        elif choice == "4":
            print("Have a nice day! :)")
            break
        else:
            print("Invalid choice. Try again.")
        

        
main()