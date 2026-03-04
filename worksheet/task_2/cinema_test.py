"""
This is where you should write your code and this is what you need to upload to Gradescope for autograding.

You must NOT change the function definitions (names, arguments).

You can run the functions you define in this file by using test.py (python test.py)
Please do not add any additional code underneath these functions.
"""

import sqlite3


def customer_tickets(conn, customer_id):
    """
    Return a list of tuples:
    (film_title, screen, price)

    Include only tickets purchased by the given customer_id.
    Order results by film title alphabetically.
    """

    query = """
    SELECT f.title, s.screen, t.price
    FROM films f JOIN screenings s ON f.film_id = s.film_id
    JOIN tickets t ON s.screening_id = t.screening_id
    WHERE t.customer_id = ?
    ORDER BY title;

"""
    
    cursor = conn.execute(query, (customer_id,))
    results = cursor.fetchall()

    print("-" *55)
    print(f"{'Film Title':<20} | {'Screen':<12} | {'Price':<12}")
    print("-" *55)
    for title, screen, price in results:
        print(f"{title:<20} | {screen:<12} | {price:<12.2f}")
    print("-" *55)
    pass


def screening_sales(conn):
    """
    Return a list of tuples:
    (screening_id, film_title, tickets_sold)

    Include all screenings, even if tickets_sold is 0.
    Order results by tickets_sold descending.
    """
    query = '''
    SELECT s.screening_id, f.title, COUNT(t.ticket_id) AS tickets_sold
    FROM films f JOIN screenings s ON f.film_id = s.film_id
    LEFT JOIN tickets t ON s.screening_id = t.screening_id
    GROUP BY s.screening_id, f.title
    ORDER BY tickets_sold DESC

'''
    cursor = conn.execute(query)
    results = cursor.fetchall()

    print("-" * 55)
    print(f"{'Screening ID':<12} | {'Film Title':<20} | {'Tickets Sold':<12}")
    print("-" * 55)
    for screening_id, title, tickets_sold in results:
        print(f"{screening_id:<12} | {title:<20} | {tickets_sold:<12}")
    print("-" * 55)
    pass


def top_customers_by_spend(conn, limit):
    """
    Return a list of tuples:
    (customer_name, total_spent)

    total_spent is the sum of ticket prices per customer.
    Only include customers who have bought at least one ticket.
    Order by total_spent descending.
    Limit the number of rows returned to `limit`.
    """
    query = ''' 
    SELECT c.customer_name, SUM(t.price) AS total_spent
    FROM tickets t JOIN customers c ON t.customer_id = c.customer_id
    GROUP BY c.customer_name
    HAVING COUNT(t.ticket_id) > 0
    ORDER BY total_spent DESC
    LIMIT ?;

'''
    cursor = conn.execute(query, (limit,))
    results = cursor.fetchall()

    print("-" * 40)
    print(f"{'Customer Name':<20} | {'Total Spent':<12}")
    print("-" * 40)
    for customer_name, total_spent in results:
        print(f"{customer_name:<20} | {total_spent:<12.2f}")
    print("-" * 40)
    pass