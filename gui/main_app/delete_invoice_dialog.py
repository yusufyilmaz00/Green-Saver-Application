from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from database.operations import get_all_invoices, delete_invoice

class DeleteInvoiceDialog(QDialog):
    def __init__(self, subscription_no):
        super().__init__()

        self.subscription_no = subscription_no

        self.setWindowTitle("Delete Invoice")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        # Invoice selection
        self.invoice_label = QLabel("Select Invoice to Delete:")
        self.invoice_combo = QComboBox()
        layout.addWidget(self.invoice_label)
        layout.addWidget(self.invoice_combo)

        # Load invoices into the dropdown
        self.populate_invoices()

        # Buttons
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_invoice)
        layout.addWidget(self.delete_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

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
                self.invoice_combo.addItem(f"Invoice No: {invoice[0]} - {invoice[1]}")

    def delete_invoice(self):
        """ Deletes the selected invoice from the database. """
        selected_invoice = self.invoice_combo.currentText()
        if "No invoices available" in selected_invoice:
            QMessageBox.warning(self, "Warning", "No invoices to delete.")
            return

        invoice_no = int(selected_invoice.split(":")[1].split("-")[0].strip())

        success, error = delete_invoice(self.subscription_no, invoice_no)
        if success:
            QMessageBox.information(self, "Success", f"Invoice {invoice_no} deleted successfully!")
            self.close()
        else:
            QMessageBox.critical(self, "Error", error)
