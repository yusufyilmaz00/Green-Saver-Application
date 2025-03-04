from PyQt5.QtWidgets import QDialog, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHeaderView
from database.operations import get_all_invoices

class ShowAllInvoicesDialog(QDialog):
    def __init__(self, subscription_no):
        super().__init__()

        self.setWindowTitle("My Invoices")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        label = QLabel("Your Invoices:")
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Invoice No", "Invoice Type", "Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_table(subscription_no)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def populate_table(self, subscription_no):
        invoices, error = get_all_invoices(subscription_no)

        if error:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Error"))
            self.table.setItem(0, 1, QTableWidgetItem(error))
            return

        if not invoices:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("No invoices found"))
            return

        self.table.setRowCount(len(invoices))
        for row_idx, (invoice_no, invoice_type, amount) in enumerate(invoices):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(invoice_no)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(invoice_type))
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{amount:.2f}"))
