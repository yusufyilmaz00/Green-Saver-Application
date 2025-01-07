import psycopg2

# PostgreSQL bağlantısı
def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="greensaverdb",
            user="postgres",
            password="1234"
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def test_connection():
    conn = create_connection()
    if conn:  # Bağlantı başarılıysa
        try:
            cursor = conn.cursor()
            # PostgreSQL versiyon sorgusu
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            print("PostgreSQL version:", result[0])  # Versiyon bilgisi yazdırılır
        except Exception as e:
            print(f"Query failed: {e}")
        finally:
            conn.close()
            print("Connection closed.")
    else:
        print("Failed to connect to the database.")

test_connection()