import sqlite3
from collections import Counter
from datetime import datetime

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

    query = '''
    SELECT customer_name, 
    COUNT(order_id) AS TotalOrders, 
    SUM(order_total) AS TotalSpent
    FROM customers c JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY customer_name
    ORDER BY customer_name;
'''
    cursor = conn.execute(query)
    results = cursor.fetchall()

    print(f"{'Customer Name':<30} | {'Total Orders':<12} | {'Total Spent':<12}")
    
    print("-" * 75)  # Print a separator line for readability
    for customer_name, TotalOrders, TotalSpent in results:
        print(f"{customer_name:<30} | {TotalOrders:<12} | {TotalSpent:<12.2f}")
    pass


def driver_workload(conn):

    query = '''
    SELECT driver_name, COUNT(delivery_id) AS deliveries_completed
    FROM drivers d JOIN deliveries de ON d.driver_id = de.driver_id
    GROUP by driver_name
    ORDER by driver_name;
'''
    cursor = conn.execute(query)
    results = cursor.fetchall()

    print(f" {'Driver Name':<30} | {'Deliveries Completed':<12}")
    for driver_name, total_deliveries in results:
        print(f"{driver_name:<30} | {total_deliveries:<12}")
    pass


def delivery_lookup_by_id(conn, order_id):

    try:
        order_id= int(order_id)
        query = '''
        SELECT o.order_id, c.customer_name, o.order_total, de.delivery_date, d.driver_name
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN deliveries de ON o.order_id = de.order_id
        JOIN drivers d ON de.driver_id = d.driver_id
        WHERE o.order_id=?;
        '''
        cursor = conn.execute(query,(order_id,))
        result= cursor.fetchone()

        if result:
            print(f"\nOrder ID : {result[0]}")
            print(f"Customer Name : {result[1]}")
            print(f"Order Total : {result[2]:.2f}")
            print(f"Delivery  Date : {result[3]}")
            print(f"Driver : {result[4]}")
        else:
            print(f"Order {order_id} not found")
    except ValueError:
        print("Invalid input")
        
    pass


# ==================================================
# Section 3 – Time-based Summaries
# ==================================================

def orders_per_date(conn):

    query = '''
    SELECT COUNT(order_id) ,order_date
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    '''
    cursor = conn.execute(query)
    result = cursor.fetchall()

    print(f"{'Order Date':<12} | {'Total Orders':<12}")
    print("-" * 35)
    
    for row in result:
        print(f"{row[1]:<12} | {row[0]:<12}")
    pass


def deliveries_per_date(conn):
    
    query = '''
    SELECT delivery_date, COUNT(delivery_id)
    FROM deliveries
    GROUP BY delivery_date
    ORDER BY delivery_date;

'''
    cursor = conn.execute(query)
    result = cursor.fetchall()

    print(f"{'Delivery Date':<12} | {'Total Deliveries':<12}")
    print("-" * 35)
    
    for row in result:
        print(f"{row[0]:<12} | {row[1]:<12}")
    pass



def customer_signups_per_month(conn):

    query = '''
    Select signup_date
    FROM customers;

'''

    cursor = conn.execute(query)
    results = cursor.fetchall()
    
    signup_dates = [row[0] for row in results]

    months = []
    for signup_date in signup_dates:
        month_year = signup_date[:7]
        months.append(month_year)

    month_counts = Counter(months)

    print(f"{'Month':<10} | {'Signups Count'}")
    print("-" * 30)
    for month, count in sorted(month_counts.items()):
        print(f"{month:<10} | {count:<15}")
        
    pass


# ==================================================
# Section 4 – Performance and Rankings
# ==================================================

def top_customers_by_spend(conn, limit=5):

    query = '''
    SELECT customer_name, SUM(order_total) AS TotalSpent
    FROM customers c JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY customer_name
    ORDER BY TotalSpent DESC
    LIMIT  ?;

    '''
    cursor = conn.execute(query, (limit,))
    results = cursor.fetchall()

    print(f"{'Customer Name':<30} | {'Total Spent':<12}")
    print("-" * 50)  

    for customer, total_spent in results:
        print(f"{customer:<30} {total_spent:<12.2f}")
    pass


def rank_drivers_by_deliveries(conn):

    query = '''
    SELECT d.driver_name, d.driver_id, COUNT(delivery_id) AS completed_deliveries
    FROM drivers d JOIN deliveries de ON d.driver_id = de.driver_id
    GROUP BY d.driver_id, d.driver_name
    ORDER BY completed_deliveries DESC
'''
    cursor = conn.execute(query)
    results = cursor.fetchall()
    
    print(f"{'Driver Name':<30} | {'Driver ID':<12} | {'Total Deliveries':<12}")
    print("-" * 75) 

    for driver_name, driver_id, total_deliveries in results:
        print(f"{driver_name:<30} | {driver_id:<12} | {total_deliveries:<12}")
    pass


def high_value_orders(conn, threshold):
    
    try:
        threshold= float(threshold)
        
        query = '''
        SELECT order_id, order_total
        FROM orders
        WHERE order_total > ?

        '''

        
        cursor = conn.execute(query,(threshold,))
        results= cursor.fetcall()

        if results:
            print(f"orders above ${threshold}")
            for order_id, order_total in results:
                print(f" Order ID: {order_id}, Total: {order_total}")
            else:
                print("No orders above that value")

    except ValueError:
        print(f"Invalid Value")

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