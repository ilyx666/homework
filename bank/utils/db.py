import psycopg2


def save_transaction_to_db(transaction_data):
    conn = psycopg2.connect("dbname=banking user=postgres password=123")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO transactions (sender_id, initial_amount, currency, receiver_id, amount_in_rub)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (
        transaction_data["sender_id"],
        transaction_data["initial_amount"],
        transaction_data["currency"],
        transaction_data["receiver_id"],
        transaction_data["amount_in_rub"]
    ))
    conn.commit()
    cursor.close()
    conn.close()