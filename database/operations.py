import random
from database.connection import get_connection, close_connection
from database.queries import *

def validate_login(subscription_no, password):
    """ Validates user login credentials. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(VALIDATE_LOGIN, (subscription_no, password))
        result = cursor.fetchone()
        return (True, "Login successful!") if result else (False, "Invalid subscriber number or password.")
    except Exception as e:
        return False, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def get_user_info(subscription_no):
    """ Fetches the full name or company name of the subscriber. """
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(GET_USER_INFO, (subscription_no, subscription_no, subscription_no))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None
    finally:
        close_connection(conn)

def update_password(subscriber_no, new_password):
    """ Updates the password of a subscriber. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_PASSWORD, (subscriber_no, new_password))
        conn.commit()
        return True, "Password updated successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def insert_individual_subscriber(fname, lname, password, id_number, birthday, address, email, phone_number):
    """ Inserts a new individual subscriber and returns their subscription number. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!", None

    try:
        cursor = conn.cursor()
        cursor.execute(INSERT_INDIVIDUAL_SUBSCRIBER, (fname, lname, id_number, birthday, address, email, phone_number, password))
        sub_no = cursor.fetchone()[0]
        conn.commit()
        return True, "Individual subscriber registered successfully!", sub_no
    except Exception as e:
        conn.rollback()
        return False, f"An error occurred: {e}", None
    finally:
        close_connection(conn)

def insert_corporate_subscriber(corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password):
    """ Inserts a new corporate subscriber and returns the subscription number. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!", None

    try:
        cursor = conn.cursor()
        cursor.execute(INSERT_CORPORATE_SUBSCRIBER, (corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password))
        sub_no = cursor.fetchone()[0]  # Fetch the generated subscription number
        conn.commit()
        return True, "Corporate subscriber registered successfully!", sub_no
    except Exception as e:
        conn.rollback()
        return False, f"An error occurred: {e}", None
    finally:
        close_connection(conn)

def get_subscriber_type(subscription_no):
    """ Retrieves the subscriber type (Individual 'I' or Corporate 'C'). """
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(GET_SUBSCRIBER_TYPE, (subscription_no,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching subscriber type: {e}")
        return None
    finally:
        close_connection(conn)

def calculate_invoice_amount(invoice_type, consumption_amount, subscriber_type):
    """ Calculates the invoice amount based on the subscriber type and consumption. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(CALCULATE_INVOICE_AMOUNT, (subscriber_type, invoice_type))
        result = cursor.fetchone()

        if not result:
            return None, "Unit price not found for the given invoice type."

        unit_price = float(result[0])  # Convert unit price to float
        consumption_amount = float(consumption_amount)  # Convert consumption to float
        invoice_amount = unit_price * consumption_amount  # Multiply to get final amount
        return invoice_amount, None
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def insert_invoice(invoice_date, subscription_no, invoice_type, consumption_amount, subscriber_type):
    """ Inserts an invoice for the subscriber. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(INSERT_INVOICE, (invoice_date, subscription_no, invoice_type, consumption_amount, None))
        conn.commit()
        return True, "Invoice successfully inserted!"
    except Exception as e:
        conn.rollback()
        return False, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def calculate_carbon_emission(subscription_no):
    """ Calculates the carbon emission for the given subscription number. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(CALCULATE_CARBON_EMISSION, (subscription_no,))
        result = cursor.fetchall()  # Fetch all records
        return result, None  # Return successful result
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def get_all_invoices(subscriber_no):
    """ Retrieves all invoices for a given subscriber. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(GET_ALL_INVOICES, (subscriber_no,))
        results = cursor.fetchall()
        return results, None
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def delete_invoice(subscriber_no, invoice_no):
    """ Deletes an invoice for a given subscriber. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(DELETE_INVOICE, (subscriber_no, invoice_no))
        conn.commit()
        return True, "Invoice deleted successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def update_invoice(invoice_no, invoice_type, invoice_amount, consumption_amount):
    """ Updates an existing invoice. """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_INVOICE, (invoice_no, invoice_type, invoice_amount, consumption_amount))
        conn.commit()
        return True, "Invoice updated successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def get_current_consumption(invoice_no):
    """ Retrieves the consumption amount for a given invoice. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(GET_CURRENT_CONSUMPTION, (invoice_no,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def get_top_spenders():
    """ Retrieves the top spenders from the database. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(GET_TOP_SPENDERS)
        results = cursor.fetchall()
        return results, None
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def get_invoice(invoice_no):
    """ Retrieves a specific invoice based on the invoice number. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(GET_INVOICE, (invoice_no,))
        results = cursor.fetchall()
        return results, None
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

# Recommendation messages dictionary
recommendation_messages = {
    "high_usage": [
        "Your usage is too high! Your recent usage has increased noticeably. Consider small changes like turning off lights when leaving a room or fixing leaky faucets.",
        "Your usage is too high! Higher consumption detected. Check for potential inefficiencies like running appliances unnecessarily or undetected leaks in water or gas systems.",
        "Your usage is higher than usual. Ensure that heating and cooling systems are used efficiently, and avoid leaving them on when not needed.",
        "Your usage is too high! Consider adopting energy-saving habits, such as using appliances during off-peak hours or minimizing hot water usage when possible."
    ],
    "low_usage": [
        "Your usage is lower than before! Great job reducing your usage! Keep it up by continuing to use resources wisely and fixing any minor leaks or drafts.",
        "Your consumption is lower than before. Maintain this trend by using only what you need and avoiding wastage.",
        "Your usage is lower than before! You're doing well with resource conservation! Consider exploring further savings, such as using water-saving fixtures or energy-efficient appliances.",
        "Your usage is lower than before! Reduced usage is a great achievement. You can also try simple habits like shortening shower times or unplugging unused devices to save even more."
    ],
    "equal_usage": [
        "Your usage remains steady. To optimize, consider checking your home for energy or water waste opportunities, like drafts or minor leaks.",
        "Your consumption is consistent. You might find savings by upgrading insulation, improving thermostat settings, or using water-efficient fixtures.",
        "Your usage remains consistent! Maintaining stable usage is good! Look for opportunities to cut back further, such as switching to eco-friendly appliances or monitoring usage more closely.",
        "Your usage remains consistent! Steady usage is a solid start. To enhance efficiency, think about scheduling routine maintenance for your systems and appliances."
    ]
}

def get_recommendation_message(consumption_difference):
    """ Returns a recommendation message based on consumption difference. """
    if consumption_difference > 0:  # Increased usage
        messages = recommendation_messages["high_usage"]
    elif consumption_difference < 0:  # Decreased usage
        messages = recommendation_messages["low_usage"]
    else:  # Same usage
        messages = recommendation_messages["equal_usage"]

    return random.choice(messages)  # Select a random message

def compare_last_two_months_with_message(subscriber_no, invoice_type):
    """ Compares the last two months' invoices and provides a recommendation message. """
    conn = get_connection()
    if not conn:
        return None, None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(COMPARE_LAST_TWO_MONTHS, (subscriber_no, invoice_type))
        result = cursor.fetchone()

        if not result:
            return None, None, "No invoice data found for the given subscriber and type."

        consumption_difference = result[0]
        recommendation_message = get_recommendation_message(consumption_difference)

        return consumption_difference, recommendation_message, None
    except Exception as e:
        return None, None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def compare_all_time_average_with_message(subscriber_no, invoice_type):
    """ Compares last month's consumption with the all-time average and provides a recommendation message. """
    conn = get_connection()
    if not conn:
        return None, None, "Database connection failed!"

    try:
        cursor = conn.cursor()

        # Retrieve last month's invoice
        cursor.execute("""
            SELECT consumptionAmount 
            FROM invoice i
            WHERE i.subNumber = %s AND i.invoiceType = %s
            ORDER BY invoiceDate DESC
            LIMIT 1;
        """, (subscriber_no, invoice_type))
        last_invoice_result = cursor.fetchone()

        if not last_invoice_result or last_invoice_result[0] is None:
            return None, None, "No recent invoice data found for the given subscriber and type."

        last_consumption = last_invoice_result[0]

        # Retrieve all-time average consumption
        cursor.execute(COMPARE_ALL_TIME_AVERAGE, (subscriber_no, invoice_type))
        average_result = cursor.fetchone()

        if not average_result or average_result[0] is None:
            return None, None, "No average consumption data found for the given subscriber and type."

        average_consumption = average_result[0]

        # Calculate difference
        consumption_difference = last_consumption - average_consumption

        # Generate recommendation message
        recommendation_message = get_recommendation_message(consumption_difference)

        return consumption_difference, recommendation_message, None
    except Exception as e:
        return None, None, f"An error occurred: {e}"
    finally:
        close_connection(conn)

def get_all_subscribers():
    """ Retrieves all subscribers from the database. """
    conn = get_connection()
    if not conn:
        return None, "Database connection failed!"

    try:
        cursor = conn.cursor()
        cursor.execute(GET_ALL_SUBSCRIBERS)
        results = cursor.fetchall()
        return results, None
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        close_connection(conn)
