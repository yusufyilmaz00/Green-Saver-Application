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

# Giriş doğrulama fonksiyonu
def validate_login(subscription_no, password):
    """
    Subscriber tablosunda verilen abone numarası ve şifreyi kontrol eder.
    """
    if len(subscription_no) != 9 or not subscription_no.isdigit():
        return False, "Subscriber number must be a 9-digit number."
    
    if len(password) > 20:
        return False, "Password must not exceed 20 characters."

    conn = create_connection()
    if not conn:
        return False, "Database connection failed!"

    try:
        cursor = conn.cursor()
        query = """
            SELECT * FROM Subscriber
            WHERE subscriptionNo = %s AND userpassword = %s;
        """
        cursor.execute(query, (subscription_no, password))
        result = cursor.fetchone()

        if result:  # Abone bulundu
            return True, "Login successful!"
        else:  # Abone numarası veya şifre hatalı
            return False, "Invalid subscriber number or password."
    except Exception as e:
        return False, f"An error occurred: {e}"
    finally:
        conn.close()