from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from gui.admin.top_spenders_dialog import TopSpendersDialog  # Import top spenders dialog
from gui.admin.all_subscribers_dialog import AllSubscribersDialog  # Import all subscribers dialog

class AdminPanelWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Panel")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        # Welcome message
        label = QLabel("Welcome to the Admin Panel!")
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(label)

        # Button to get top spenders
        self.get_top_spenders_button = QPushButton("Get Top Spenders")
        self.get_top_spenders_button.clicked.connect(self.open_top_spenders_window)
        layout.addWidget(self.get_top_spenders_button)

        # Button to view all subscribers
        self.view_all_subscribers_button = QPushButton("View All Subscribers")
        self.view_all_subscribers_button.clicked.connect(self.open_all_subscribers_window)
        layout.addWidget(self.view_all_subscribers_button)

        # Logout Button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def open_top_spenders_window(self):
        """ Opens the top spenders dialog. """
        dialog = TopSpendersDialog()
        dialog.exec_()

    def open_all_subscribers_window(self):
        """ Opens the all subscribers dialog. """
        dialog = AllSubscribersDialog()
        dialog.exec_()

    def logout(self):
        """ Logs out the admin and closes the panel. """
        self.close()
