from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from database.operations import validate_login, get_user_info, get_subscriber_type
from gui.main_app.main_app_window import MainAppWindow  # Import the main application window
from gui.auth.password_update_dialog import PasswordUpdateDialog  # Import password update dialog

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 400, 300)

        form_layout = QFormLayout()
        self.subscription_no_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Subscriber Number:", self.subscription_no_input)
        form_layout.addRow("Password:", self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.reset_button = QPushButton("Reset Password")  # New button for password reset
        self.reset_button.clicked.connect(self.open_update_password_dialog)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_window)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def login(self):
        subscription_no = self.subscription_no_input.text()
        password = self.password_input.text()

        # GUI-level validation before sending the request to the database
        if len(subscription_no) != 9 or not subscription_no.isdigit():
            QMessageBox.warning(self, "Input Error", "Subscriber number must be a 9-digit number.")
            return

        if len(password) > 20:
            QMessageBox.warning(self, "Input Error", "Password must not exceed 20 characters.")
            return

        # If input is valid, proceed with database validation
        valid, message = validate_login(subscription_no, password)
        if valid:
            QMessageBox.information(self, "Login Successful", message)
            self.open_main_app(subscription_no)
        else:
            QMessageBox.warning(self, "Login Failed", message)

    def open_main_app(self, subscription_no):
        """ Opens the main application window after successful login. """
        user_info = get_user_info(subscription_no)

        if not user_info:
            QMessageBox.critical(self, "Error", "User information could not be retrieved. Please check the subscription number.")
            return

        subscriber_type = get_subscriber_type(subscription_no)
        if not subscriber_type:
            QMessageBox.critical(self, "Error", "Subscriber type could not be determined. Please contact support.")
            return

        self.main_app = MainAppWindow(user_info, subscription_no, subscriber_type)
        self.main_app.show()
        self.close()

    def open_update_password_dialog(self):
        """ Opens the password update dialog. """
        dialog = PasswordUpdateDialog()
        dialog.exec_()

    def close_window(self):
        """ Closes the login window. """
        self.close()
