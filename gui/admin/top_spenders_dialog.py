from PyQt5.QtWidgets import QDialog, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHeaderView
from database.operations import get_top_spenders

class TopSpendersDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Top Spenders")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        label = QLabel("Top Spenders (Avg Invoice > 20):")
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Subscriber Number", "Average Invoice Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_table()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def populate_table(self):
        """ Fetches top spenders from the database and fills the table. """
        results, error = get_top_spenders()

        if error:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Error"))
            self.table.setItem(0, 1, QTableWidgetItem(error))
            return

        self.table.setRowCount(len(results))
        for row_idx, (sub_number, avg_invoice_amount) in enumerate(results):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(sub_number)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{avg_invoice_amount:.2f}"))
