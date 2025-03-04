from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from gui.auth.user_login_window import LoginWindow
from gui.auth.admin_login_window import AdminLoginWindow
from gui.subscriptions.corporate_window import CorporateWindow  # Import corporate subscription window
from gui.subscriptions.individual_window import IndividualWindow  # Import individual subscription window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Green Saver")
        self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(QIcon("app_icon.png"))

        layout = QVBoxLayout()
        
        title_label = QLabel("Reduce Your Consumption, Save Your Wallet!\nWelcome to the Green Saver System!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green; margin-bottom: 20px;")
        layout.addWidget(title_label)

        self.login_button = QPushButton("Subscriber Login")
        self.admin_login_button = QPushButton("Admin Login")
        self.register_corporate_button = QPushButton("Register Corporate Subscription")
        self.register_individual_button = QPushButton("Register Individual Subscription")
        self.exit_button = QPushButton("Exit Program")

        self.login_button.setFixedSize(250, 50)
        self.admin_login_button.setFixedSize(250, 50)
        self.register_corporate_button.setFixedSize(250, 50)
        self.register_individual_button.setFixedSize(250, 50)
        self.exit_button.setFixedSize(250, 50)
        self.exit_button.setStyleSheet("background-color: red; color: white;")

        self.login_button.clicked.connect(self.open_login_window)
        self.admin_login_button.clicked.connect(self.open_admin_login_window)
        self.register_corporate_button.clicked.connect(self.open_corporate_window)
        self.register_individual_button.clicked.connect(self.open_individual_window)
        self.exit_button.clicked.connect(self.close_application)

        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.admin_login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_corporate_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_individual_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    def open_admin_login_window(self):
        self.admin_login_window = AdminLoginWindow()
        self.admin_login_window.show()

    def open_corporate_window(self):
        """ Opens the corporate subscription registration window. """
        self.register_corporate_window = CorporateWindow()
        self.register_corporate_window.show()

    def open_individual_window(self):
        """ Opens the individual subscription registration window. """
        self.register_individual_window = IndividualWindow()
        self.register_individual_window.show()

    def close_application(self):
        reply = QMessageBox.question(self, "Exit Program", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
