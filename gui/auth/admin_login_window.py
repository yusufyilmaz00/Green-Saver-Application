from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout
from gui.admin_panel_window import AdminPanelWindow  # Import the admin panel window

class AdminLoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Login")
        self.setGeometry(300, 300, 400, 200)

        self.correct_username = "admin"
        self.correct_password = "1111"

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_window)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_login(self):
        """ Validates admin credentials and opens the admin panel. """
        username = self.username_input.text()
        password = self.password_input.text()

        if username == self.correct_username and password == self.correct_password:
            QMessageBox.information(self, "Login Successful", "Welcome to Admin Panel!")
            self.open_admin_panel()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_admin_panel(self):
        """ Opens the admin panel window upon successful login. """
        self.admin_panel = AdminPanelWindow()
        self.admin_panel.show()
        self.close()

    def close_window(self):
        """ Closes the admin login window. """
        self.close()
