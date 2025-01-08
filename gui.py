from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, 
    QFormLayout, QLineEdit, QHBoxLayout, QMessageBox ,QComboBox, QDialog, 
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView
)    
from PyQt5.QtCore import QDate
from database import DatabaseManager
from datetime import datetime

#Ana pencereyi yönetir ve diğer pencerelere geçiş sağlar.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Project")
        self.setGeometry(100, 100, 400, 300)

        # Main window layout
        layout = QVBoxLayout()

        # Buttons
        self.login_button = QPushButton("Login")
        self.register_corporate_button = QPushButton("Corporate Subscription")
        self.register_individual_button = QPushButton("Individual Subscription")

        # Button click events
        self.login_button.clicked.connect(self.open_login_window)
        self.register_corporate_button.clicked.connect(self.open_corporate_window)
        self.register_individual_button.clicked.connect(self.open_individual_window)

        # Add buttons to layout
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_corporate_button)
        layout.addWidget(self.register_individual_button)

        # Set layout to main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    def open_corporate_window(self):
        self.register_corporate_window = CorporateWindow()
        self.register_corporate_window.show()

    def open_individual_window(self):
        self.register_individual_window = IndividualWindow()
        self.register_individual_window.show()

#Kullanıcı giriş ekranı.
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 400, 300)

        # Form layout for user input
        form_layout = QFormLayout()

        # Input fields
        self.subscription_no_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Add fields to form layout
        form_layout.addRow("Subscriber Number:", self.subscription_no_input)
        form_layout.addRow("Password:", self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_window)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def login(self):
        subscription_no = self.subscription_no_input.text()
        password = self.password_input.text()
        db_manager = DatabaseManager()

        valid, message = db_manager.validate_login(subscription_no, password)
        if valid:
            QMessageBox.information(self, "Login Successful", message)
            self.open_main_app(subscription_no)
        else:
            QMessageBox.warning(self, "Login Failed", message)

    def open_main_app(self, subscription_no):
        db_manager = DatabaseManager()
        user_info = db_manager.get_user_info(subscription_no)

        if not user_info:
            QMessageBox.critical(self, "Error", "User information could not be retrieved. Please check the subscription number.")
            return

        subscriber_type = db_manager.get_subscriber_type(subscription_no)
        if not subscriber_type:
            QMessageBox.critical(self, "Error", "Subscriber type could not be determined. Please contact support.")
            return

        self.main_app = MainAppWindow(user_info, subscription_no, subscriber_type, db_manager)
        self.main_app.show()
        self.close()


    def close_window(self):
        self.close()


#Bireysel abonelik kayıt ekranı.
class IndividualWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Individual Subscription")
        self.setGeometry(200, 200, 400, 500)

        # Form layout for user input
        form_layout = QFormLayout()

        # Input fields
        self.firstname_input = QLineEdit()
        self.lastname_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.id_number_input = QLineEdit()
        self.birthdate_input = QLineEdit()
        self.address_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()

        # Add fields to form layout
        form_layout.addRow("First Name:", self.firstname_input)
        form_layout.addRow("Last Name:", self.lastname_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("ID Number:", self.id_number_input)
        form_layout.addRow("Birthdate (YYYY-MM-DD):", self.birthdate_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_window)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def save_data(self):
        # Alınan verileri doğrula
        fname = self.firstname_input.text()
        lname = self.lastname_input.text()
        password = self.password_input.text()
        id_number = self.id_number_input.text()
        birthdate = self.birthdate_input.text()
        address = self.address_input.text()
        email = self.email_input.text()
        phone_number = self.phone_input.text()

        if not self.validate_input(fname, lname, password, id_number, birthdate, address, email, phone_number):
            return

        # DatabaseManager ile veritabanına kaydet
        db_manager = DatabaseManager()
        success, message, subscription_no = db_manager.insert_individual_subscriber(
            fname, lname, password, id_number, birthdate, address, email, phone_number
        )

        if success:
            QMessageBox.information(
                self,
                "Success",
                f"{message}\nYour subscription number is: {subscription_no}"
            )
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)

    def validate_input(self, fname, lname, password, id_number, birthdate, address, email, phone_number):
        # Alanların doluluğunu kontrol et
        if not all([fname, lname, password, id_number, birthdate, address, email, phone_number]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return False

        # Uzunluk kontrolleri
        if len(fname) > 30 or len(lname) > 30 or len(password) > 20:
            QMessageBox.warning(self, "Input Error", "Name, password lengths are invalid!")
            return False
        if len(id_number) != 11 or not id_number.isdigit():
            QMessageBox.warning(self, "Input Error", "ID Number must be 11 digits!")
            return False
        if len(phone_number) != 10 or not phone_number.isdigit():
            QMessageBox.warning(self, "Input Error", "Phone Number must be 10 digits!")
            return False
        if len(address) > 100 or len(email) > 50:
            QMessageBox.warning(self, "Input Error", "Address or email exceeds length limit!")
            return False

        # Tarih formatı kontrolü
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid birthdate format! Use YYYY-MM-DD.")
            return False

        return True

    def close_window(self):
        self.close()

#Kurumsal abonelik kayıt ekranı.
class CorporateWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Corporate Subscription")
        self.setGeometry(200, 200, 400, 600)

        # Form layout for user input
        form_layout = QFormLayout()

        # Input fields
        self.corporate_name_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.tax_no_input = QLineEdit()
        self.corporate_type_input = QLineEdit()
        self.foundation_date_input = QLineEdit()
        self.address_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_number_input = QLineEdit()

        # Add fields to form layout
        form_layout.addRow("Corporate Name:", self.corporate_name_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Tax Number:", self.tax_no_input)
        form_layout.addRow("Corporate Type:", self.corporate_type_input)
        form_layout.addRow("Foundation Date (YYYY-MM-DD):", self.foundation_date_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_number_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_window)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def save_data(self):
        # Alınan verileri doğrula
        corporate_name = self.corporate_name_input.text()
        password = self.password_input.text()
        tax_no = self.tax_no_input.text()
        corporate_type = self.corporate_type_input.text()
        foundation_date = self.foundation_date_input.text()
        address = self.address_input.text()
        email = self.email_input.text()
        phone_number = self.phone_number_input.text()

        # Doğrulama
        if not self.validate_input(corporate_name, password, tax_no, corporate_type, foundation_date, address, email, phone_number):
            return

        # Veritabanına bağlan ve veriyi kaydet
        db_manager = DatabaseManager()
        success, message, subscription_no = db_manager.insert_corporate_subscriber(
            corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password
        )

        if success:
            QMessageBox.information(
                self,
                "Success",
                f"{message}\nYour subscription number is: {subscription_no}"
            )
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)

    def validate_input(self, corporate_name, password, tax_no, corporate_type, foundation_date, address, email, phone_number):
        # Boş alanların kontrolü
        if not all([corporate_name, password, tax_no, corporate_type, foundation_date, address, email, phone_number]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return False

        # Uzunluk kontrolleri
        if len(corporate_name) > 40:
            QMessageBox.warning(self, "Input Error", "Corporate name must not exceed 40 characters.")
            return False
        if len(password) > 20:
            QMessageBox.warning(self, "Input Error", "Password must not exceed 20 characters.")
            return False
        if len(tax_no) != 10 or not tax_no.isdigit():
            QMessageBox.warning(self, "Input Error", "Tax Number must be a 10-digit number.")
            return False
        if len(corporate_type) > 40:
            QMessageBox.warning(self, "Input Error", "Corporate type must not exceed 40 characters.")
            return False
        if len(phone_number) != 10 or not phone_number.isdigit():
            QMessageBox.warning(self, "Input Error", "Phone Number must be a 10-digit number.")
            return False
        if len(address) > 100:
            QMessageBox.warning(self, "Input Error", "Address must not exceed 100 characters.")
            return False
        if len(email) > 50:
            QMessageBox.warning(self, "Input Error", "Email must not exceed 50 characters.")
            return False

        # Tarih formatı kontrolü
        try:
            datetime.strptime(foundation_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid foundation date format! Use YYYY-MM-DD.")
            return False

        return True

    def close_window(self):
        self.close()

# Kullanıcının giriş yaptıktan sonra ulaşabileceği ana uygulama ekranı.
class MainAppWindow(QWidget):

    def __init__(self, user_info, subscription_no, subscriber_type, db_manager):
        super().__init__()

        self.subscription_no = subscription_no
        self.subscriber_type = subscriber_type
        self.db_manager = db_manager

        self.setWindowTitle("Main Application")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Kullanıcı bilgisi (Hoş geldiniz mesajı)
        welcome_label = QLabel(f"Hoşgeldiniz, {user_info}")
        welcome_label.setStyleSheet("color: blue; font-size: 16px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Diğer butonlar
        self.button1 = QPushButton("Insert Invoice")
        self.button1.clicked.connect(self.insert_invoice)
        
        self.button2 = QPushButton("Calculate Carbon Emission")  # Yeni buton
        self.button2.clicked.connect(self.open_carbon_emission_window)

        self.button3 = QPushButton("Show My Invoices")  # Yeni buton
        self.button3.clicked.connect(self.show_invoice_window)

        self.buttonX = QPushButton("Logout")
        self.buttonX.clicked.connect(self.logout)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)  
        layout.addWidget(self.button3)
        layout.addWidget(self.buttonX)

        self.setLayout(layout)

    def insert_invoice(self):
        dialog = InvoiceDialog(self.db_manager, self.subscription_no, self.subscriber_type)
        if dialog.exec_():
            print("Invoice details saved successfully.")

    def open_carbon_emission_window(self):
        dialog = CarbonEmissionDialog(self.db_manager, self.subscription_no)
        dialog.exec_()

    def show_invoice_window(self):
        QMessageBox.information(self, "Invoices", "Success")

    def logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.close()


class InvoiceDialog(QDialog):
    def __init__(self, db_manager, subscription_no, subscriber_type):
        super().__init__()
        self.db_manager = db_manager
        self.subscription_no = subscription_no
        self.subscriber_type = subscriber_type

        self.setWindowTitle("Invoice Insert")
        self.setGeometry(100, 100, 300, 200)

        # Create layout
        layout = QVBoxLayout()

        # Invoice Date
        self.date_label = QLabel("Invoice Date:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMaximumDate(QDate.currentDate())  # Tarih kısıtlaması

        # Invoice Type
        self.type_label = QLabel("Invoice Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Electricity", "Water", "Natural Gas"])

        # Consumption Amount
        self.amount_label = QLabel("Consumption Amount:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.clicked.connect(self.save_invoice)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # Add widgets to layout
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_invoice(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        invoice_type = self.type_combo.currentText()
        amount = self.amount_input.text()

        if not amount:
            QMessageBox.warning(self, "Input Error", "Please enter the consumption amount.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                QMessageBox.warning(self, "Input Error", "Consumption amount must be a positive number.")
                return

            # Faturayı veritabanına ekle
            success, message = self.db_manager.insert_invoice(date, self.subscription_no, invoice_type, amount, self.subscriber_type)
            if success:
                QMessageBox.information(self, "Invoice Saved", message)
                self.accept()
            else:
                QMessageBox.critical(self, "Error", message)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Consumption amount must be a valid number.")

class CarbonEmissionDialog(QDialog):
    def __init__(self, db_manager, subscription_no):
        super().__init__()
        self.db_manager = db_manager
        self.subscription_no = subscription_no

        self.setWindowTitle("Carbon Emission")
        self.setGeometry(200, 200, 600, 400)

        # Tablo widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Invoice No", "Carbon Emission (kg)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Veritabanından veri al ve tabloyu güncelle
        self.populate_table()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    # Veritabanından karbon emisyonu verilerini alır ve tabloya ekler.
    def populate_table(self):
        result, error = self.db_manager.calculate_carbon_emission(self.subscription_no)
        if error:
            QMessageBox.critical(self, "Error", error)
            return

        # Tabloya verileri ekle
        self.table.setRowCount(len(result))
        for row_idx, (invoice_no, carbon_emission) in enumerate(result):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(invoice_no)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{carbon_emission:.2f}"))