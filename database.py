import psycopg2

class DatabaseManager:

    def __init__(self, host="localhost", database="greensaverdb", user="postgres", password="1234"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    #Veritabanı bağlantısı oluşturur ve döndürür.    
    def create_connection(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.connection
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None
    # Mevcut veritabanı bağlantısını kapatır.
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
        self.connection = None

    # Veritabanına bağlanmayı test eder ve PostgreSQL versiyonunu kontrol eder.
    def test_connection(self):
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # PostgreSQL versiyon sorgusu
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
                print("PostgreSQL version:", result[0])  # Versiyon bilgisi yazdırılır
            except Exception as e:
                print(f"Query failed: {e}")
            finally:
                self.close_connection()
        else:
            print("Failed to connect to the database.")

    # Giriş doğrulama fonksiyonu
    def validate_login(self, subscription_no, password):
        if len(subscription_no) != 9 or not subscription_no.isdigit():
            return False, "Subscriber number must be a 9-digit number."

        if len(password) > 20:
            return False, "Password must not exceed 20 characters."

        conn = self.create_connection()
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
            self.close_connection()

    def insert_individual_subscriber(self, fname, lname, password, id_number, birthday, address, email, phone_number):
        conn = self.create_connection()
        if not conn:
            return False, "Database connection failed!", None

        try:
            cursor = conn.cursor()

            # SQL fonksiyonunu çağır ve abone numarasını al
            query = """
                SELECT insert_individual_subscriber(
                    %s, %s, %s, %s, CURRENT_DATE, %s, %s, %s, %s
                );
            """
            cursor.execute(query, (fname, lname, id_number, birthday, address, email, phone_number, password))
            sub_no = cursor.fetchone()[0]  # SQL fonksiyonundan dönen abone numarası
            conn.commit()
            return True, "Individual subscriber registered successfully!", sub_no
        except Exception as e:
            conn.rollback()
            return False, f"An error occurred: {e}", None
        finally:
            self.close_connection()

    def insert_corporate_subscriber(self, corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password):
        conn = self.create_connection()
        if not conn:
            return False, "Database connection failed!", None

        try:
            cursor = conn.cursor()

            # SQL fonksiyonunu çağır ve abone numarasını al
            query = """
                SELECT insert_corporate_subscriber(
                    %s, %s, %s, %s, CURRENT_DATE, %s, %s, %s, %s
                );
            """
            cursor.execute(query, (corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password))
            sub_no = cursor.fetchone()[0]  # SQL fonksiyonundan dönen abone numarası
            conn.commit()
            return True, "Corporate subscriber registered successfully!", sub_no
        except Exception as e:
            conn.rollback()
            return False, f"An error occurred: {e}", None
        finally:
            self.close_connection()
