import psycopg2
from database.config import DB_CONFIG

def get_connection():
    """ PostgreSQL veritabanı bağlantısını oluşturur ve döndürür. """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def close_connection(conn):
    """ Veritabanı bağlantısını kapatır. """
    if conn:
        conn.close()
