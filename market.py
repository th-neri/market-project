import json

file_name = "market_file.json"

#load products from the JSON file
def load_items():
    with open(file_name, "r") as file:
        return json.load(file)
    
#save products back to JSON file
def save_item(items):
    with open(file_name, "w") as file:
        json.dump(items, file, indent=4)

#show products
def show_items(items):
    if len(items) == 0:
        print("No products available.")
    else:
        print("\n---Products available to buy---")
        for i in items:
            print(f'{i["id"]}- {i["name"]} | Price: {i["price"]} | Stock: {i["stock"]}')

#function to add any product desired
def add_item(items):
    name = input("Write the product name: ").strip()
    price = float(input("Write the product price: ").strip())
    stock = int(input("Write the product stock: ").strip())
    id_product = max([i["id"] for i in items], default=0) + 1
    # to add the product information to the json file
    items.append({"id": id_product, "name": name, "price": price, "stock": stock})
    save_item(items)
    print("Product saved successfully.")

#function to find the product by the ID
def find_product(items, item_id):
    for i in items:
        if i["id"] == item_id:
            return i
    return None

#function to buy products
def buy_item(items):
    items = load_items()
    cart = []
    total = 0

    while True:
        show_items(items)
        choose_product = input("\nEnter the product by the ID number(or Q to quit): ").strip().lower()
        if choose_product == "q":
            final_price = discount_price(total)  
            if final_price != total:
                print(f"Discount applied! Now the final price is: {final_price:.2f}.")
            else:
                print(f"The total purchase is: ${final_price:.2f}.")
            break
        try:
            item_id = int(choose_product)
            item = find_product(items, item_id)

            if item:
                quantity = int(input("Enter the quantity: ").strip())

                if quantity <= item["stock"]:
                    item["stock"] -= quantity
                    cost = quantity * item["price"]
                    total += cost
                    cart.append((item["name"], quantity, cost))
                    print(f'{item["name"]} added to the cart!')
                else:
                    print(f'Not enough {item["name"]} in the stock. Only {item["stock"]} available.')
            else:
                print("Product not found.")
        except ValueError:
            print("Invalid input.")

        save_item(items)

        print("\n---Total---")
        for item in cart:
            print(f"{item[0]} x{item[1]} = ${item[2]}")  
        print(f"TOTAL: ${total:.2f}")

#function for different discounts according to each price
def discount_price(total):
    if total >= 100:
        return total * 0.85
    elif total >= 80:
        return total * 0.90
    elif total >= 50:
        return total * 0.95
    else:
        return total
    
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