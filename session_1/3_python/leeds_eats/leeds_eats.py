import sqlite3

# ==================================================
# Section 1 – Summaries
# ==================================================
conn = sqlite3.connect("food_delivery.db")

def total_customers(conn):

    query = '''
    SELECT COUNT(customer_id)
    FROM customers

    '''
    cursor = conn.execute(query)
    results = cursor.fetchone() 

    print(f"There are {results[0]} customers")
    pass


def customer_signup_range(conn):
    
    query ='''
    SELECT MIN(signup_date), MAX(signup_date)
    FROM customers;

    '''
    cursor = conn.execute(query)
    results= cursor.fetchone()

    earliest = results[0]
    latest = results[1]

    print(f"The earliest customer sign up date was {earliest}\n"
          f"The latest customer sign up date was {latest}")
    pass


def order_summary_stats(conn):

    query ='''
    SELECT COUNT(order_id), AVG(order_total), MIN(order_total), Max(order_total)
    FROM orders;

    '''
    cursor = conn.execute(query)
    total_orders, avg_order, min_order, max_order = cursor.fetchone()

    print(f"Total orders: {total_orders}\n"
          f"Average order price: {avg_order}\n"
          f"Lowest order total: {min_order}\n"
          f"Highest order total: {max_order}")
    pass


def driver_summary(conn):

    count_query = '''
    SELECT COUNT(driver_id)
    FROM drivers
    
    '''
    cursor = conn.execute(count_query)
    total_drivers = cursor.fetchone()
    
    hire_dates_query = '''
    SELECT hire_date
    FROM drivers

    '''
    cursor = conn.execute(hire_dates_query)
    results = cursor.fetchall()

    print(f"Total drivers: {total_drivers[0]}")
    print("Hire dates:")
    
    for hire_date in results:
        print(f"- {hire_date[0]}")
    pass


# ==================================================
# Section 2 – Key Statistics
# ==================================================

def orders_per_customer(conn):
    pass


def driver_workload(conn):
    pass


def delivery_lookup_by_id(conn, order_id):
    pass


# ==================================================
# Section 3 – Time-based Summaries
# ==================================================

def orders_per_date(conn):
    pass


def deliveries_per_date(conn):
    pass


def customer_signups_per_month(conn):
    pass


# ==================================================
# Section 4 – Performance and Rankings
# ==================================================

def top_customers_by_spend(conn, limit=5):
    pass


def rank_drivers_by_deliveries(conn):
    pass


def high_value_orders(conn, threshold):
    pass


# ==================================================
# Menus - You should not need to change any code below this point until the stretch tasks.
# ==================================================

def section_1_menu(conn):
    while True:
        print("\nSection 1 – Summaries")
        print("1. Total number of customers")
        print("2. Customer signup date range")
        print("3. Order summary statistics")
        print("4. Driver summary")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            total_customers(conn)
        elif choice == "2":
            customer_signup_range(conn)
        elif choice == "3":
            order_summary_stats(conn)
        elif choice == "4":
            driver_summary(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_2_menu(conn):
    while True:
        print("\nSection 2 – Key Statistics")
        print("1. Orders per customer")
        print("2. Driver workload")
        print("3. Order delivery overview")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_customer(conn)
        elif choice == "2":
            driver_workload(conn)
        elif choice == "3":
            order_id = input("Enter order ID: ").strip()
            if not order_id.isdigit():
                print("Please enter a valid integer order ID.")
                continue
            delivery_lookup_by_id(conn, int(order_id))
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_3_menu(conn):
    while True:
        print("\nSection 3 – Time-based Summaries")
        print("1. Orders per date")
        print("2. Deliveries per date")
        print("3. Customer signups per month")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_date(conn)
        elif choice == "2":
            deliveries_per_date(conn)
        elif choice == "3":
            customer_signups_per_month(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_4_menu(conn):
    while True:
        print("\nSection 4 – Performance and Rankings")
        print("1. Top 5 customers by total spend")
        print("2. Rank drivers by deliveries completed")
        print("3. High-value orders")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            top_customers_by_spend(conn)
        elif choice == "2":
            rank_drivers_by_deliveries(conn)
        elif choice == "3":
            try:
                threshold = float(input("Enter order value threshold (£): "))
                high_value_orders(conn, threshold)
            except:
                print("Please enter a valid numerical value.")
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def main_menu(conn):
    while True:
        print("\n=== Delivery Service Management Dashboard ===")
        print("1. Section 1 – Summaries")
        print("2. Section 2 – Key Statistics")
        print("3. Section 3 – Time-based Summaries")
        print("4. Section 4 – Performance and Rankings")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            section_1_menu(conn)
        elif choice == "2":
            section_2_menu(conn)
        elif choice == "3":
            section_3_menu(conn)
        elif choice == "4":
            section_4_menu(conn)
        elif choice == "0":
            print("Exiting dashboard.")
            break
        else:
            print("Invalid option. Please try again.")

def get_connection(db_path="food_delivery.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    conn = get_connection()
    main_menu(conn)
    conn.close()