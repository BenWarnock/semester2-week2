
""" Your name: Ben Warnock
Your student ID: 201852300
You state that the code submitted is wholly written by yourself. 
Date: 22/02/2026 """

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

    pass
    return results

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

    pass
    return results
    


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

    pass
    return results