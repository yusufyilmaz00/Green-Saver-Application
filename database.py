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
    def get_current_consumption(self, invoice_no):
        """
        Verilen fatura numarasına göre mevcut tüketim miktarını döndürür.
        :param invoice_no: Fatura numarası
        :return: Mevcut tüketim miktarı veya None (hata durumunda)
        """
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = """
                SELECT consumptionAmount
                FROM invoice
                WHERE invoiceNo = %s;
            """
            cursor.execute(query, (invoice_no,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Tüketim miktarını döndür
            else:
                return None  # Fatura bulunamadıysa None döndür
        except Exception as e:
            print(f"An error occurred while fetching consumption amount: {e}")
            return None
        finally:
            self.close_connection()

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

    def compare_all_time_average_with_message(self, subscriber_no, invoice_type):
        """
        Son ayki fatura tüketimi ile tüm faturaların ortalama tüketimini karşılaştırır ve öneri mesajı döndürür.
        :param subscriber_no: Abone numarası
        :param invoice_type: Fatura türü
        :return: (tüketim farkı, öneri mesajı), hata
        """
        conn = self.create_connection()
        if not conn:
            return None, None, "Database connection failed!"

        try:
            cursor = conn.cursor()

            # Son ayki faturayı al
            last_invoice_query = """
                SELECT consumptionAmount 
                FROM invoice i
                WHERE i.subNumber = %s AND i.invoiceType = %s
                ORDER BY invoiceDate DESC
                LIMIT 1;
            """
            cursor.execute(last_invoice_query, (subscriber_no, invoice_type))
            last_invoice_result = cursor.fetchone()

            if not last_invoice_result or last_invoice_result[0] is None:
                return None, None, "No recent invoice data found for the given subscriber and type."

            last_consumption = last_invoice_result[0]

            # Tüm faturaların ortalama tüketimini al
            average_query = """
                SELECT calc_all_time_avg_consumptionAmount(%s, %s);
            """
            cursor.execute(average_query, (subscriber_no, invoice_type))
            average_result = cursor.fetchone()

            if not average_result or average_result[0] is None:
                return None, None, "No average consumption data found for the given subscriber and type."

            average_consumption = average_result[0]

            # Son ay tüketimi ile ortalama tüketim arasındaki farkı hesapla
            consumption_difference = last_consumption - average_consumption

            # Öneri mesajını al
            recommendation_message = self.get_recommendation_message(consumption_difference)

            return consumption_difference, recommendation_message, None
        except Exception as e:
            return None, None, f"An error occurred: {e}"
        finally:
            self.close_connection()

    def get_all_subscribers(self):
        """
        Veritabanındaki 'all_sub_view' view'inden tüm aboneleri döndürür.
        :return: [(subscriptionno, subName, subscribertype)], error
        """
        conn = self.create_connection()
        if not conn:
            return None, "Database connection failed!"

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM all_sub_view;"
            cursor.execute(query)
            results = cursor.fetchall()
            return results, None
        except Exception as e:
            return None, f"An error occurred: {e}"
        finally:
            self.close_connection()
