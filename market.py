import json

file_name = "market_file.json"
file_name2 = "users.json"

#load products from the JSON file
def load_items():
    with open(file_name, "r") as file:
        return json.load(file)
    
#save products back to JSON file
def save_item(items):
    with open(file_name, "w") as file:
        json.dump(items, file, indent=4)

#load user information from the JSON file
def load_users():
    with open(file_name2, "r") as user_file:
        return json.load(user_file)
    
#save user information back to JSON file
def save_user(users):
    with open(file_name2, "w") as user_file:
        json.dump(users, user_file, indent=4)

#show products
def show_items(items):
    if len(items) == 0:
        print("No products available.")
    else:
        for i in items:
            print(f'{i["id"]}- {i["name"]} | Price: {i["price"]} | Stock: {i["stock"]}')

#function to add the user information
def add_user(users):
    users = load_users()
    name = input("Enter the username: ").strip()
    password = input("Enter the password: ").strip()
    user_id = max([u["user_id"] for u in users], default=0) + 1
    # to add the user information to the JSON file
    users.append({"user_id": user_id, "name": name, "password": password, "total_spent": 0})
    save_user(users)
    print("User information saved successfully.")

def login_user(users):
    name = input("Username: ").strip()
    password = input("Password: ").strip()

    for user in users:
        if user["name"] == name and user["password"] == password:
            print(f'Welcome, {user["name"]}! Feel free to choose any option. :)')
            return user
        
    print("Invalid username or password. Try again or create an account.")
    return None

#function to add any product desired
def add_item(items):
    name = input("Write the product name: ").strip()
    price = float(input("Write the product price: ").strip())
    stock = int(input("Write the product stock: ").strip())
    id_product = max([i["id"] for i in items], default=0) + 1
    # to add the product information to the JSON file
    items.append({"id": id_product, "name": name, "price": price, "stock": stock})
    save_item(items)
    print("Product saved successfully.")

#function to erase a product desired
def delete_item(items):
    show_items(items)  

    try:
        item_id = int(input("Choose the product you want to erase by the ID: ").strip())
        item = find_product(items, item_id)

        if item is None:
            print("Product not found.")
            return
        while True:
            choice = input(f'Are you sure you want to erase {item["name"]} (Y/N)? ').strip().lower()
            if choice == "y":
                items.remove(item)
                save_item(items)
                print(f'{item["name"]} erased successfully!')
                break
            elif choice == "n":
                print("Canceled.")
                break
            else:
                print("Invalid choice.")
    except ValueError:
        print("Invalid input.")
            
#function to find the product by the ID
def find_product(items, item_id):
    for i in items:
        if i["id"] == item_id:
            return i
    return None

#function to buy products
def buy_item(items, user):
    cart = []
    total = 0

    while True:
        show_items(items)
        choose_product = input("\nEnter the product by the ID number(or Q to quit): ").strip().lower()
        if choose_product == "q":
            final_price = discount_price(total)  
            if final_price != total:
                print(f'Thanks for coming, {user["name"]}! A discount has been applied and now the final price is: {final_price:.2f}.')
            else:
                print(f'Thanks for coming, {user["name"]}! The total purchase is: ${final_price:.2f}.')
            break
        try:
            item_id = int(choose_product)
            item = find_product(items, item_id)

            if item:
                quantity = int(input("Enter the quantity: ").strip())

                if quantity <= item["stock"]:
                    item["stock"] -= quantity
                    save_item(items)
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

        final_price = discount_price(total)
        user["total_spent"] += final_price

        users = load_users()
        for u in users:
            if u["user_id"] == user["user_id"]:
                u["total_spent"] = user["total_spent"]
        save_user(users)

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
    users = load_users()
    current_user = None

    while True:
        if not current_user:
            print("\n---User options---")
            print("1. Create your account")
            print("2. Login")
            print("3. Leave")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_user(users)
            elif choice == "2":
                current_user = login_user(users)
            elif choice == "3":
                print("Have a nice day! :)")
                break
            else:
                print("Invalid choice. Try again.")

        else:
            print("\n---Market options---")
            print("1. View products")
            print("2. Add product")
            print("3. Erase product")
            print("4. Buy product")
            print("5. Logout")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print("\n---Products available to buy---")
                items = load_items()
                show_items(items)
            elif choice == "2":
                add_item(items)
            elif choice == "3":
                print("\n---Choose the product you want to erase: ---")
                delete_item(items)
            elif choice == "4":
                buy_item(items, current_user)
            elif choice == "5":
                print("Thanks for coming. Have a nice day! :)")
                current_user = None
                continue
            else:
                print("Invalid choice. Try again.")
              
main()