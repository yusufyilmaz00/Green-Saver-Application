import psycopg2,random

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

    # kullanıcı ismini alan fonksiyon
    def get_user_info(self, subscription_no):
        conn = self.create_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            # Abone tipini kontrol et ve gerekli bilgiyi al
            query = """
                SELECT 
                    CASE 
                        WHEN subscriberType = 'I' THEN (SELECT fname || ' ' || lname FROM individualSubscriber WHERE subscriptionNo = %s)
                        WHEN subscriberType = 'C' THEN (SELECT corporateName FROM corporateSubscriber WHERE subscriptionNo = %s)
                    END AS display_name
                FROM Subscriber
                WHERE subscriptionNo = %s;
            """
            cursor.execute(query, (subscription_no, subscription_no, subscription_no))
            result = cursor.fetchone()

            if result:
                return result[0]  # İsim veya şirket adı
            return None
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return None
        finally:
            self.close_connection()
    # kullanıcı şifresini güncelleme fonksiyonu
    def update_password(self, subscriber_no, new_password):
        conn = self.create_connection()
        if not conn:
            return False, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT update_password(%s, %s);
            """
            cursor.execute(query, (subscriber_no, new_password))
            conn.commit()
            return True, "Password updated successfully!"
        except Exception as e:
            conn.rollback()
            return False, f"An error occurred: {e}"
        finally:
            if conn:
                conn.close()

    # bireysel abone ekleme fonksiyonu
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

# işlev fonksiyonları

    def get_subscriber_type(self, subscription_no):
        conn = self.create_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT subscriberType FROM Subscriber WHERE subscriptionNo = %s;"
            cursor.execute(query, (subscription_no,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching subscriber type: {e}")
            return None
        finally:
            self.close_connection()

    def calculate_invoice_amount(self, invoice_type, consumption_amount, subscriber_type):
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    CASE 
                        WHEN %s = 'C' THEN corporationPrice
                        ELSE individualPrice
                    END AS unit_price
                FROM energy
                WHERE invoiceType = %s;
            """
            cursor.execute(query, (subscriber_type, invoice_type))
            result = cursor.fetchone()

            if not result:
                return None, "Unit price not found for the given invoice type."

            unit_price = float(result[0])  # Birim fiyatı float'a çevirin
            consumption_amount = float(consumption_amount)  # Tüketim miktarını float'a çevirin
            invoice_amount = unit_price * consumption_amount  # Çarpımı gerçekleştirin
            return invoice_amount, None
        except Exception as e:
            return None, f"An error occurred: {e}"
        finally:
            self.close_connection()


    def insert_invoice(self, invoice_date, subscription_no, invoice_type, consumption_amount, subscriber_type):
        invoice_amount, error = self.calculate_invoice_amount(invoice_type, consumption_amount, subscriber_type)
        if error:
            return False, error

        conn = self.create_connection()
        if not conn:
            return False, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT insert_invoice(%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (invoice_date, subscription_no, invoice_type, consumption_amount, invoice_amount))
            conn.commit()
            return True, "Invoice successfully inserted!"
        except Exception as e:
            conn.rollback()
            return False, f"An error occurred: {e}"
        finally:
            self.close_connection()

    # Kullanıcı abonelik numarasına göre her bir faturanın karbon emisyonunu hesaplar.
    def calculate_carbon_emission(self, subscription_no):
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM calculate_carbon_emission(%s);
            """
            cursor.execute(query, (subscription_no,))
            result = cursor.fetchall()  # Tüm kayıtları al
            return result, None  # Başarılı sonuç döndür
        except Exception as e:
            return None, f"An error occurred: {e}"
        finally:
            self.close_connection()

# Kullanıcının tüm faturalarını gösteren fonksiyon.Bireysel veya kurumsal kullanıcıya göre SQL fonksiyonunu çalıştırır.
    def get_all_invoices(self, subscriber_no):
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            # Kullanıcının abone tipini al
            cursor = conn.cursor()
            query_type = "SELECT subscriberType FROM Subscriber WHERE subscriptionNo = %s;"
            cursor.execute(query_type, (subscriber_no,))
            subscriber_type = cursor.fetchone()

            if not subscriber_type:
                return None, "Subscriber type not found."

            subscriber_type = subscriber_type[0]  # 'I' (Individual) veya 'C' (Corporate)

            # Doğru SQL fonksiyonunu çağır
            if subscriber_type == 'I':
                query = "SELECT get_all_individualInvoices(%s);"
            elif subscriber_type == 'C':
                query = "SELECT get_all_corporateInvoices(%s);"
            else:
                return None, "Invalid subscriber type."

            cursor.execute(query, (subscriber_no,))

            # `RAISE INFO` mesajlarını yakala
            conn.commit()  # PostgreSQL işlemini tamamla
            messages = conn.notices  # RAISE INFO ile dönen mesajları al
            if not messages:
                return None, "No messages received from the database."

            return messages, None
        except Exception as e:
            return None, f"An error occurred: {e}"
        finally:
            if conn:
                conn.close()

    def delete_invoice(self, subscriber_no, invoice_no):
        conn = self.create_connection()
        if not conn:
            return False, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT delete_invoice(%s, %s);
            """
            cursor.execute(query, (subscriber_no, invoice_no))
            conn.commit()
            return True, "Invoice deleted successfully!"
        except Exception as e:
            conn.rollback()
            return False, f"An error occurred: {e}"
        finally:
            if conn:
                conn.close()

    def update_invoice(self, invoice_no, invoice_type, invoice_amount, consumption_amount):
        conn = self.create_connection()
        if not conn:
            return False, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT update_invoice(%s, %s, %s, %s);
            """
            cursor.execute(query, (invoice_no, invoice_type, invoice_amount, consumption_amount))
            conn.commit()
            return True, "Invoice updated successfully!"
        except Exception as e:
            conn.rollback()
            print(f"Database error in update_invoice: {e}")
            return False, f"An error occurred: {e}"
        finally:
            if conn:
                conn.close()

    def get_top_spenders(self):
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM get_top_spenders();"
            cursor.execute(query)
            results = cursor.fetchall()  # Tüm sonuçları al
            return results, None
        except Exception as e:
            print(f"Database error in get_top_spenders: {e}")
            return None, f"An error occurred: {e}"
        finally:
            if conn:
                conn.close()

    # Verilen fatura numarasına göre faturayı getirir.
    def get_invoice(self, invoice_no):
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM get_invoice(%s);"
            cursor.execute(query, (invoice_no,))
            results = cursor.fetchall()  # Tüm sonuçları al
            return results, None
        except Exception as e:
            print(f"Database error in get_invoice: {e}")
            return None, f"An error occurred: {e}"
        finally:
            if conn:
                conn.close()

    # Öneri mesajlarını tanımlayan yapı
    recommendation_messages = {
        "high_usage": [
            "Your recent usage is significantly higher. Consider reducing unnecessary consumption.",
            "Energy-saving tips: Turn off unused appliances to lower your bill.",
            "Your energy usage has increased! Inspect possible leaks or inefficiencies."
        ],
        "low_usage": [
            "Good job! Your usage has decreased compared to the previous month.",
            "Keep up the energy-efficient habits to save even more.",
            "Your reduced consumption is great for both your wallet and the environment."
        ],
        "equal_usage": [
            "Your consumption is consistent. Consider optimizing further to save costs."
        ]
    }

    # Yeni öneri mesajı fonksiyonu
    def get_recommendation_message(self, consumption_difference):
        """
        Fatura tüketim farkına göre öneri mesajını döndürür.
        :param consumption_difference: İki fatura arasındaki tüketim farkı
        :return: Rastgele bir öneri mesajı
        """
        if consumption_difference > 0:  # Fazla tüketim
            messages = self.recommendation_messages["high_usage"]
        elif consumption_difference < 0:  # Az tüketim
            messages = self.recommendation_messages["low_usage"]
        else:  # Eşit tüketim
            messages = self.recommendation_messages["equal_usage"]
            return messages[0]  # Sabit mesaj döndür

        return random.choice(messages)  # Rastgele mesaj seç
    
    def compare_last_two_months_with_message(self, subscriber_no, invoice_type):
        """
        Son iki faturayı karşılaştırır ve bir öneri mesajı döndürür.
        :param subscriber_no: Abone numarası
        :param invoice_type: Fatura türü
        :return: (fatura farkı, öneri mesajı), hata
        """
        conn = self.create_connection()
        if not conn:
            return None, None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT last_two_months_invoice(%s, %s);
            """
            cursor.execute(query, (subscriber_no, invoice_type))
            result = cursor.fetchone()

            if not result:
                return None, None, "No invoice data found for the given subscriber and type."

            consumption_difference = result[0]
            recommendation_message = self.get_recommendation_message(consumption_difference)

            return consumption_difference, recommendation_message, None
        except Exception as e:
            return None, None, f"An error occurred: {e}"
        finally:
            self.close_connection()

