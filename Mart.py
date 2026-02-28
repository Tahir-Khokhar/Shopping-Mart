import csv
import os
from datetime import datetime, timedelta

# ---------- FILES ----------
MANAGER_FILE = "managers.csv"
CUSTOMER_FILE = "customers.csv"
PRODUCT_FILE = "products.csv"
SALES_FILE = "sales.csv"
MANAGER_BUY_FILE = "manager_buy.csv"  # NEW: record manager purchases

# ---------- HELPERS ----------
def file_exists(filename):
    return os.path.exists(filename)

def manager_exists():
    if not file_exists(MANAGER_FILE):
        return False
    with open(MANAGER_FILE, "r") as f:
        return any(csv.reader(f))

# ---------- MANAGER ----------
def register_manager():
    if manager_exists():
        print("Manager already exists. Cannot register another.")
        return
    name = input("Enter manager name: ")
    pin = input("Enter 4-digit pin: ")
    if not pin.isdigit() or len(pin) != 4:
        print("Pin must be 4 digits")
        return
    with open(MANAGER_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name, pin])
    print("Manager registered successfully")

def manager_login():
    print("\n1. Login\n2. Register")
    choice = input("Choose: ")
    if choice == "2":
        register_manager()
        return
    if not manager_exists():
        print("No manager registered. Please register first.")
        return
    name = input("Manager name: ")
    pin = input("Pin: ")
    with open(MANAGER_FILE, "r") as f:
        for row in csv.reader(f):
            if row == [name, pin]:
                manager_menu(name)  # pass manager name for purchase record
                return
    print("Invalid credentials")

def manager_menu(manager_name):
    while True:
        print("\n--- MANAGER MENU ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Wallet / Earnings")
        print("4. Record Manager Purchase")
        print("5. Back")
        choice = input("Choose: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            wallet_menu()
        elif choice == "4":
            manager_buy(manager_name)
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def add_product():
    name = input("Product name: ").lower()
    price = input("Price in $ per unit: ").replace('$','').strip()
    unit = input("Unit (kg / piece): ")
    stock = input("Stock quantity: ")
    if not price.isdigit() or not stock.isdigit():
        print("Price and stock must be numbers")
        return
    with open(PRODUCT_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name, price, unit, stock, 0])
    print(f"Product added successfully: {name} ${price} per {unit}, stock: {stock}")

def view_products():
    if not file_exists(PRODUCT_FILE):
        print("No products found")
        return
    print("\n--- PRODUCTS ---")
    with open(PRODUCT_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            print(f"{row[0]} | ${row[1]} per {row[2]} | Stock: {row[3]} | Sold today: {row[4]}")

# ---------- WALLET ----------
def record_sale(amount):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(SALES_FILE, "a", newline="") as f:
        csv.writer(f).writerow([today, amount])

def wallet_menu():
    while True:
        print("\n--- WALLET ---")
        print("1. Current Balance")
        print("2. Daily Sales Records")
        print("3. Earnings per Day/Week/Month/Year")
        print("4. Back")
        choice = input("Choose: ")
        if choice == "1":
            show_current_balance()
        elif choice == "2":
            show_daily_sales()
        elif choice == "3":
            show_earnings()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

def show_current_balance():
    total = 0
    if file_exists(SALES_FILE):
        with open(SALES_FILE, "r") as f:
            for row in csv.reader(f):
                if row and row[1].isdigit():
                    total += int(row[1])
    print(f"Current balance in mart: ${total}")

def show_daily_sales():
    if not file_exists(SALES_FILE):
        print("No sales yet")
        return
    print("\n--- DAILY SALES ---")
    sales_dict = {}
    with open(SALES_FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[1].isdigit():
                date, amount = row
                sales_dict[date] = sales_dict.get(date, 0) + int(amount)
    for date, amount in sales_dict.items():
        print(f"{date}: ${amount}")

def show_earnings():
    if not file_exists(SALES_FILE):
        print("No sales yet")
        return
    print("\n--- EARNINGS ---")
    today = datetime.now().date()
    daily_total = {}
    weekly_total = 0
    monthly_total = 0
    yearly_total = 0
    with open(SALES_FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[1].isdigit():
                date_str, amount = row
                amount = int(amount)
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                daily_total[date_str] = daily_total.get(date_str, 0) + amount
                if today - timedelta(days=7) <= date_obj <= today:
                    weekly_total += amount
                if date_obj.month == today.month and date_obj.year == today.year:
                    monthly_total += amount
                if date_obj.year == today.year:
                    yearly_total += amount
    print("Daily totals:")
    for d, amt in daily_total.items():
        print(f"{d}: ${amt}")
    print(f"Weekly total: ${weekly_total}")
    print(f"Monthly total: ${monthly_total}")
    print(f"Yearly total: ${yearly_total}")

# ---------- MANAGER PURCHASE RECORD ----------
def manager_buy(manager_name):
    if not file_exists(MANAGER_BUY_FILE):
        print("No purchase records found.")
        return

    date_input = input("Enter date to view purchases (YYYY-MM-DD): ")
    print(f"\n--- Purchases by {manager_name} on {date_input} ---")
    found_any = False

    with open(MANAGER_BUY_FILE, "r") as f:
        for row in csv.reader(f):
            if len(row) >= 5 and row[0] == manager_name and row[1] == date_input:
                print(f"Product: {row[2]}, Quantity: {row[3]}, Total Cost: {row[4]}")
                found_any = True

    if not found_any:
        print("No purchases found on this date.")

# ---------- CUSTOMER ----------
def customer_exists(name):
    if not file_exists(CUSTOMER_FILE):
        return False
    with open(CUSTOMER_FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[0] == name:
                return True
    return False

def register_customer():
    name = input("Enter name to register: ")
    if customer_exists(name):
        print("Already registered")
        return
    with open(CUSTOMER_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name])
    print("Registration successful")

def customer_login():
    name = input("Enter your name: ")
    if not customer_exists(name):
        print("User not found. Please register first.")
        return
    print("Login successful")
    buy_products()

def buy_products():
    if not file_exists(PRODUCT_FILE):
        print("No products available")
        return
    products = list(csv.reader(open(PRODUCT_FILE)))
    total = 0
    while True:
        print("\nAvailable products:")
        for p in products:
            if len(p) < 5:
                continue
            print(f"{p[0]} | ${p[1]} per {p[2]} | Stock: {p[3]}")
        item = input("Product name: ").lower()
        found = False
        for p in products:
            if len(p) < 5:
                continue
            if p[0] == item:
                qty = int(input("Quantity: "))
                if qty > int(p[3]):
                    print("Not enough stock")
                    found = True
                    break
                cost = qty * int(p[1])
                total += cost
                p[3] = str(int(p[3]) - qty)
                p[4] = str(int(p[4]) + qty)
                found = True
                break
        if not found:
            print("Product not found")
        more = input("Buy more? (yes/no): ").lower()
        if more != "yes":
            break
    with open(PRODUCT_FILE, "w", newline="") as f:
        csv.writer(f).writerows(products)
    print(f"Total bill: ${total}")
    payment = int(input("Payment ($): "))
    if payment >= total:
        print(f"Payment successful. Change: ${payment - total}")
        record_sale(total)
    else:
        print("Not enough money")

def customer_menu():
    print("\n1. Login\n2. Register")
    choice = input("Choose: ")
    if choice == "1":
        customer_login()
    elif choice == "2":
        register_customer()
    else:
        print("Invalid choice")

# ---------- MAIN ----------
def main_menu():
    while True:
        print("\n===== MAIN MENU =====")
        print("1. Manager\n2. Customer\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            manager_login()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

main_menu()
