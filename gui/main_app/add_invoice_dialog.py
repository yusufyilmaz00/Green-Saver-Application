from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.operations import insert_invoice

class AddInvoiceDialog(QDialog):
    def __init__(self, subscription_no, subscriber_type):
        super().__init__()

        self.subscription_no = subscription_no
        self.subscriber_type = subscriber_type

        self.setWindowTitle("Add Invoice")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Invoice Type
        self.type_label = QLabel("Invoice Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Electricity", "Water", "Natural Gas"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        # Consumption Amount
        self.amount_label = QLabel("Consumption Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        # Buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_invoice)
        layout.addWidget(self.save_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def save_invoice(self):
        invoice_type = self.type_combo.currentText()
        consumption_amount = self.amount_input.text()

        if not consumption_amount.isdigit() or int(consumption_amount) <= 0:
            QMessageBox.warning(self, "Input Error", "Consumption amount must be a positive number.")
            return

        success, message = insert_invoice("2024-02-24", self.subscription_no, invoice_type, int(consumption_amount), self.subscriber_type)

        if success:
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)
