GET_USER_INFO = """
    SELECT 
        CASE 
            WHEN subscriberType = 'I' THEN (SELECT fname || ' ' || lname FROM individualSubscriber WHERE subscriptionNo = %s)
            WHEN subscriberType = 'C' THEN (SELECT corporateName FROM corporateSubscriber WHERE subscriptionNo = %s)
        END AS display_name
    FROM Subscriber
    WHERE subscriptionNo = %s;
"""

VALIDATE_LOGIN = """
    SELECT * FROM Subscriber WHERE subscriptionNo = %s AND userpassword = %s;
"""

UPDATE_PASSWORD = """
    SELECT update_password(%s, %s);
"""

INSERT_INDIVIDUAL_SUBSCRIBER = """
    SELECT insert_individual_subscriber(%s, %s, %s, %s, CURRENT_DATE, %s, %s, %s, %s);
"""

INSERT_CORPORATE_SUBSCRIBER = """
    SELECT insert_corporate_subscriber(%s, %s, %s, %s, CURRENT_DATE, %s, %s, %s, %s);
"""

GET_SUBSCRIBER_TYPE = """
    SELECT subscriberType FROM Subscriber WHERE subscriptionNo = %s;
"""
CALCULATE_INVOICE_AMOUNT = """
    SELECT 
        CASE 
            WHEN %s = 'C' THEN corporationPrice
            ELSE individualPrice
        END AS unit_price
    FROM energy
    WHERE invoiceType = %s;
"""

CALCULATE_CARBON_EMISSION = """
    SELECT * FROM calculate_carbon_emission(%s);
"""

CALCULATE_INVOICE_AMOUNT = """
    SELECT 
        CASE 
            WHEN %s = 'C' THEN corporationPrice
            ELSE individualPrice
        END AS unit_price
    FROM energy
    WHERE invoiceType = %s;
"""

GET_ALL_INVOICES = """
    SELECT * FROM get_all_invoices(%s);
"""

GET_INVOICE = """
    SELECT * FROM get_invoice(%s);
"""

INSERT_INVOICE = """
    SELECT insert_invoice(%s, %s, %s, %s, %s);
"""

DELETE_INVOICE = """
    SELECT delete_invoice(%s, %s);
"""

UPDATE_INVOICE = """
    SELECT update_invoice(%s, %s, %s, %s);
"""

GET_CURRENT_CONSUMPTION = """
    SELECT consumptionAmount FROM invoice WHERE invoiceNo = %s;
"""

GET_TOP_SPENDERS = """
    SELECT * FROM get_top_spenders();
"""

GET_ALL_SUBSCRIBERS = """
    SELECT * FROM all_sub_view;
"""

COMPARE_LAST_TWO_MONTHS = """
    SELECT last_two_months_invoice(%s, %s);
"""

COMPARE_ALL_TIME_AVERAGE = """
    SELECT calc_all_time_avg_consumptionAmount(%s, %s);
"""
