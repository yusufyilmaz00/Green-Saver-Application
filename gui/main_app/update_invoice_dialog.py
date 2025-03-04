from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from database.operations import get_all_invoices, update_invoice, calculate_invoice_amount, get_current_consumption

class UpdateInvoiceDialog(QDialog):
    def __init__(self, subscription_no, subscriber_type):
        super().__init__()

        self.subscription_no = subscription_no
        self.subscriber_type = subscriber_type

        self.setWindowTitle("Update Invoice")
        self.setGeometry(300, 300, 600, 400)
        self.setWindowModality(True)

        layout = QVBoxLayout()

        # Invoice selection
        self.invoice_label = QLabel("Select Invoice:")
        self.invoice_combo = QComboBox()
        self.invoice_combo.addItem("-- Select an Invoice --")
        layout.addWidget(self.invoice_label)
        layout.addWidget(self.invoice_combo)

        # Populate invoices
        self.populate_invoices()

        # New invoice type selection
        self.invoice_type_label = QLabel("Select New Invoice Type:")
        self.invoice_type_combo = QComboBox()
        self.invoice_type_combo.addItems(["Electricity", "Natural Gas", "Water"])
        layout.addWidget(self.invoice_type_label)
        layout.addWidget(self.invoice_type_combo)

        # New consumption amount
        self.consumption_label = QLabel("New Consumption Amount (Optional):")
        self.consumption_input = QLineEdit()
        layout.addWidget(self.consumption_label)
        layout.addWidget(self.consumption_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_invoice)
        button_layout.addWidget(self.update_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def populate_invoices(self):
        """ Fetches invoices from the database and populates the dropdown. """
        invoices, error = get_all_invoices(self.subscription_no)
        if error:
            QMessageBox.critical(self, "Error", error)
            return

        if not invoices:
            self.invoice_combo.addItem("No invoices available")
        else:
            for invoice in invoices:
                self.invoice_combo.addItem(f"{invoice[1]} - {invoice[0]}")  # Format: "Invoice Type - Invoice No"

    def update_invoice(self):
        """ Updates the selected invoice in the database. """
        try:
            selected_invoice = self.invoice_combo.currentText()
            if selected_invoice == "-- Select an Invoice --":
                QMessageBox.warning(self, "Warning", "Please select an invoice.")
                return

            invoice_no = int(selected_invoice.split("-")[1].strip())  # Extract Invoice No
            new_type = self.invoice_type_combo.currentText()
            new_consumption = self.consumption_input.text()

            if not new_consumption:
                # Fetch the current consumption amount
                new_consumption, error = get_current_consumption(invoice_no)
                if error or new_consumption is None:
                    QMessageBox.warning(self, "Error", "Failed to fetch current consumption amount.")
                    return

            # Calculate the invoice amount
            invoice_amount, error = calculate_invoice_amount(new_type, float(new_consumption), self.subscriber_type)
            if error:
                QMessageBox.critical(self, "Error", error)
                return

            # Update the invoice
            success, message = update_invoice(invoice_no, new_type, invoice_amount, float(new_consumption))
            if success:
                QMessageBox.information(self, "Success", message)
                self.close()
            else:
                QMessageBox.critical(self, "Error", message)

        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self, "Critical Error", str(e))
