from PyQt5.QtWidgets import QDialog, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHeaderView
from database.operations import get_all_subscribers

class AllSubscribersDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("All Subscribers")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        label = QLabel("All Subscribers:")
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Subscription No", "Subscriber Name", "Subscriber Type"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_table()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def populate_table(self):
        """ Fetches all subscribers from the database and fills the table. """
        results, error = get_all_subscribers()

        if error:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Error"))
            self.table.setItem(0, 1, QTableWidgetItem(error))
            return

        self.table.setRowCount(len(results))
        for row_idx, (subscription_no, sub_name, sub_type) in enumerate(results):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(subscription_no)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(sub_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(sub_type))
