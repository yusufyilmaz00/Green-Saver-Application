import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Project")
        self.setGeometry(100, 100, 400, 300)

        # Main window layout
        layout = QVBoxLayout()

        # Buttons
        self.login_button = QPushButton("Login")
        self.corporate_button = QPushButton("Corporate Subscription")
        self.individual_button = QPushButton("Individual Subscription")

        # Button click events
        self.login_button.clicked.connect(self.open_login_window)
        self.corporate_button.clicked.connect(self.open_corporate_window)
        self.individual_button.clicked.connect(self.open_individual_window)

        # Add buttons to layout
        layout.addWidget(self.login_button)
        layout.addWidget(self.corporate_button)
        layout.addWidget(self.individual_button)

        # Set layout to main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_login_window(self):
        self.login_window = SubWindow("Login Window")
        self.login_window.show()

    def open_corporate_window(self):
        self.corporate_window = SubWindow("Corporate Subscription Window")
        self.corporate_window.show()

    def open_individual_window(self):
        self.individual_window = SubWindow("Individual Subscription Window")
        self.individual_window.show()


class SubWindow(QWidget):
    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()
        label = QLabel(f"This window is: {title}")
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
