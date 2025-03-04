from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from database.operations import compare_last_two_months_with_message

class CompareInvoicesDialog(QDialog):
    def __init__(self, subscription_no):
        super().__init__()

        self.setWindowTitle("Compare Last Two Months")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.invoice_type_label = QLabel("Select Invoice Type:")
        self.invoice_type_combo = QComboBox()
        self.invoice_type_combo.addItems(["Electricity", "Natural Gas", "Water"])
        layout.addWidget(self.invoice_type_label)
        layout.addWidget(self.invoice_type_combo)

        self.compare_button = QPushButton("Compare")
        self.compare_button.clicked.connect(self.compare_invoices)
        layout.addWidget(self.compare_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def compare_invoices(self):
        selected_type = self.invoice_type_combo.currentText()

        if not selected_type:
            QMessageBox.warning(self, "Warning", "Please select an invoice type.")
            return

        difference, message, error = compare_last_two_months_with_message(self.subscription_no, selected_type)

        if error:
            QMessageBox.critical(self, "Error", error)
        elif difference is None:
            QMessageBox.information(self, "No Data", "No invoices found for the last two months.")
        else:
            QMessageBox.information(self, "Recommendation:\n", message)

        self.close()
