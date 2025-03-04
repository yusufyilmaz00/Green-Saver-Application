from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
from database.operations import insert_corporate_subscriber
from datetime import datetime

class CorporateWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Corporate Subscription")
        self.setGeometry(200, 200, 400, 500)

        form_layout = QFormLayout()

        self.corporate_name_input = QLineEdit()
        self.tax_no_input = QLineEdit()
        self.corporate_type_input = QLineEdit()
        self.foundation_date_input = QLineEdit()
        self.address_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Corporate Name:", self.corporate_name_input)
        form_layout.addRow("Tax Number:", self.tax_no_input)
        form_layout.addRow("Corporate Type:", self.corporate_type_input)
        form_layout.addRow("Foundation Date (YYYY-MM-DD):", self.foundation_date_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_number_input)
        form_layout.addRow("Password:", self.password_input)

        self.save_button = QPushButton("Register")
        self.save_button.clicked.connect(self.save_data)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_window)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_data(self):
        """ Validates input fields and registers a corporate subscriber. """
        corporate_name = self.corporate_name_input.text().strip()
        tax_no = self.tax_no_input.text().strip()
        corporate_type = self.corporate_type_input.text().strip()
        foundation_date = self.foundation_date_input.text().strip()
        address = self.address_input.text().strip()
        email = self.email_input.text().strip()
        phone_number = self.phone_number_input.text().strip()
        password = self.password_input.text().strip()

        # Validation Checks
        if not self.validate_input(corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password):
            return

        # Database Insertion
        success, message, subscription_no = insert_corporate_subscriber(
            corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password
        )

        if success:
            QMessageBox.information(self, "Success", f"{message}\nYour subscription number is: {subscription_no}")
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)

    def validate_input(self, corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password):
        """ Validates all input fields before sending data to the database. """

        # Empty field check
        if not all([corporate_name, tax_no, corporate_type, foundation_date, address, email, phone_number, password]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return False

        # Length and format validations
        if len(corporate_name) > 40:
            QMessageBox.warning(self, "Input Error", "Corporate name must not exceed 40 characters!")
            return False

        if len(password) > 20:
            QMessageBox.warning(self, "Input Error", "Password must not exceed 20 characters!")
            return False

        if len(tax_no) != 10 or not tax_no.isdigit():
            QMessageBox.warning(self, "Input Error", "Tax Number must be exactly 10 digits!")
            return False

        if len(corporate_type) > 40:
            QMessageBox.warning(self, "Input Error", "Corporate type must not exceed 40 characters!")
            return False

        if len(phone_number) != 10 or not phone_number.isdigit():
            QMessageBox.warning(self, "Input Error", "Phone Number must be exactly 10 digits!")
            return False

        if len(address) > 100:
            QMessageBox.warning(self, "Input Error", "Address must not exceed 100 characters!")
            return False

        if len(email) > 50 or "@" not in email or "." not in email:
            QMessageBox.warning(self, "Input Error", "Invalid email format!")
            return False

        # Date validation
        try:
            datetime.strptime(foundation_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid foundation date format! Use YYYY-MM-DD.")
            return False

        return True

    def close_window(self):
        """ Closes the corporate subscription window. """
        self.close()
