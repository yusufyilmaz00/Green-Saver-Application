from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, 
    QFormLayout, QLineEdit, QHBoxLayout, QMessageBox
)
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
            self.open_main_app()
        else:
            QMessageBox.warning(self, "Login Failed", message)

    def open_main_app(self):
        self.main_app = MainAppWindow()
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
        success, message = db_manager.insert_individual_subscriber(
            fname, lname, password, id_number, birthdate, address, email, phone_number
        )
        if success:
            QMessageBox.information(self, "Success", message)
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)

    def validate_input(self, fname, lname, password, id_number, birthdate, address, email, phone_number):
        # Alanların boş olmadığını kontrol et
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

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Application")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.button1 = QPushButton("Process 1")
        self.button1.clicked.connect(self.process_1)

        self.button2 = QPushButton("Process 2")
        self.button2.clicked.connect(self.process_2)

        self.button3 = QPushButton("Logout")
        self.button3.clicked.connect(self.logout)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.setLayout(layout)

    def process_1(self):
        QMessageBox.information(self, "Process 1", "Process 1 executed!")

    def process_2(self):
        QMessageBox.information(self, "Process 2", "Process 2 executed!")

    def logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.close()
