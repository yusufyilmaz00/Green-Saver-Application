from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QFormLayout, QHBoxLayout
from database.operations import validate_login, update_password

class PasswordUpdateDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reset Password")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.subscription_no_input = QLineEdit()
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)

        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Subscriber Number:", self.subscription_no_input)
        form_layout.addRow("Old Password:", self.old_password_input)
        form_layout.addRow("New Password:", self.new_password_input)
        form_layout.addRow("Confirm New Password:", self.confirm_password_input)

        button_layout = QHBoxLayout()
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_password)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def reset_password(self):
        """ Handles password reset logic. """
        subscription_no = self.subscription_no_input.text()
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not subscription_no or not old_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields must be filled!")
            return

        if not subscription_no.isdigit() or len(subscription_no) != 9:
            QMessageBox.warning(self, "Error", "Subscriber number must be a 9-digit number.")
            return

        valid, message = validate_login(subscription_no, old_password)
        if not valid:
            QMessageBox.warning(self, "Error", "Old password is incorrect.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "New passwords do not match.")
            return

        if new_password == old_password:
            QMessageBox.warning(self, "Error", "New password cannot be the same as the old password.")
            return

        if len(new_password) > 20:
            QMessageBox.warning(self, "Error", "New password must not exceed 20 characters.")
            return

        success, update_message = update_password(subscription_no, new_password)
        if success:
            QMessageBox.information(self, "Success", update_message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", update_message)
