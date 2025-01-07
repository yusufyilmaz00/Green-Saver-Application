import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, 
    QFormLayout, QLineEdit, QHBoxLayout, QMessageBox
)
from database import *

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
        self.password_input.setEchoMode(QLineEdit.Normal)  # Şifre gösterimi

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
        # Kullanıcı girişlerini al
        subscription_no = self.subscription_no_input.text()
        password = self.password_input.text()

        # Veri tabanında kontrol et
        valid, message = validate_login(subscription_no, password)

        # Sonuçlara göre işlem yap
        if valid:
            QMessageBox.information(self, "Login Successful", message)
            self.open_main_app()  # Ana uygulama ekranına geçiş
        else:
            QMessageBox.warning(self, "Login Failed", message)

    def open_main_app(self):
        # Ana uygulama ekranını aç
        self.main_app = MainAppWindow()
        self.main_app.show()
        self.close()  # Login penceresini kapat

    def close_window(self):
        self.close()

class MainAppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Application")
        self.setGeometry(200, 200, 600, 400)

        # Ana ekran butonları
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
        self.close()  # Ana uygulama penceresini kapat

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
        self.password_input.setEchoMode(QLineEdit.Normal)  # Şifre gösterimi aktif
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
        # Get input data
        data = {
            "First Name": self.firstname_input.text(),
            "Last Name": self.lastname_input.text(),
            "Password": self.password_input.text(),
            "ID Number": self.id_number_input.text(),
            "Birthdate": self.birthdate_input.text(),
            "Address": self.address_input.text(),
            "Email": self.email_input.text(),
            "Phone Number": self.phone_input.text(),
        }

        # Display a confirmation message
        QMessageBox.information(self, "Data Saved", f"Data has been saved:\n{data}")

    def close_window(self):
        self.close()


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
        self.password_input.setEchoMode(QLineEdit.Normal)  # Şifre gösterimi aktif
        self.tax_no_input = QLineEdit()
        self.corporate_type_input = QLineEdit()
        self.foundation_date_input = QLineEdit()
        self.register_date_input = QLineEdit()
        self.address_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_number_input = QLineEdit()

        # Add fields to form layout
        form_layout.addRow("Corporate Name:", self.corporate_name_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Tax Number:", self.tax_no_input)
        form_layout.addRow("Corporate Type:", self.corporate_type_input)
        form_layout.addRow("Foundation Date (YYYY-MM-DD):", self.foundation_date_input)
        form_layout.addRow("Register Date (YYYY-MM-DD):", self.register_date_input)
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
        # Get input data
        data = {
            "Corporate Name": self.corporate_name_input.text(),
            "Password": self.password_input.text(),
            "Tax Number": self.tax_no_input.text(),
            "Corporate Type": self.corporate_type_input.text(),
            "Foundation Date": self.foundation_date_input.text(),
            "Register Date": self.register_date_input.text(),
            "Address": self.address_input.text(),
            "Email": self.email_input.text(),
            "Phone Number": self.phone_number_input.text(),
        }

        # Display a confirmation message
        QMessageBox.information(self, "Data Saved", f"Data has been saved:\n{data}")

    def close_window(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
