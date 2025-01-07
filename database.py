import psycopg2

# PostgreSQL bağlantısı
def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="your_database",
            user="your_username",
            password="your_password"
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None
