from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.operations import insert_individual_subscriber
from datetime import datetime

class IndividualWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Individual Subscription")
        self.setGeometry(200, 200, 400, 500)

        form_layout = QFormLayout()

        self.firstname_input = QLineEdit()
        self.lastname_input = QLineEdit()
        self.id_number_input = QLineEdit()
        self.birthdate_input = QLineEdit()
        self.address_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("First Name:", self.firstname_input)
        form_layout.addRow("Last Name:", self.lastname_input)
        form_layout.addRow("ID Number:", self.id_number_input)
        form_layout.addRow("Birthdate (YYYY-MM-DD):", self.birthdate_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_input)
        form_layout.addRow("Password:", self.password_input)

        self.save_button = QPushButton("Register")
        self.save_button.clicked.connect(self.save_data)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_data(self):
        """ Validates input fields and registers an individual subscriber. """
        fname = self.firstname_input.text().strip()
        lname = self.lastname_input.text().strip()
        id_number = self.id_number_input.text().strip()
        birthdate = self.birthdate_input.text().strip()
        address = self.address_input.text().strip()
        email = self.email_input.text().strip()
        phone_number = self.phone_input.text().strip()
        password = self.password_input.text().strip()

        # Validation Checks
        if not self.validate_input(fname, lname, id_number, birthdate, address, email, phone_number, password):
            return

        # Database Insertion
        success, message, subscription_no = insert_individual_subscriber(
            fname, lname, password, id_number, birthdate, address, email, phone_number
        )

        if success:
            QMessageBox.information(self, "Success", f"{message}\nYour subscription number is: {subscription_no}")
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)

    def validate_input(self, fname, lname, id_number, birthdate, address, email, phone_number, password):
        """ Validates all input fields before sending data to the database. """

        # Empty field check
        if not all([fname, lname, id_number, birthdate, address, email, phone_number, password]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return False

        # Length and format validations
        if len(fname) > 30 or len(lname) > 30:
            QMessageBox.warning(self, "Input Error", "First and Last name must not exceed 30 characters!")
            return False

        if len(password) > 20:
            QMessageBox.warning(self, "Input Error", "Password must not exceed 20 characters!")
            return False

        if len(id_number) != 11 or not id_number.isdigit():
            QMessageBox.warning(self, "Input Error", "ID Number must be exactly 11 digits!")
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
            datetime.strptime(birthdate, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid birthdate format! Use YYYY-MM-DD.")
            return False

        return True
    
    def close_window(self):
        """ Closes the individual subscription window. """
        self.close()