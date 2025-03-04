from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.operations import get_invoice

class ShowInvoiceDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Show Invoice")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        # Invoice No Input
        self.invoice_no_label = QLabel("Enter Invoice Number:")
        self.invoice_no_input = QLineEdit()
        layout.addWidget(self.invoice_no_label)
        layout.addWidget(self.invoice_no_input)

        # Buttons
        self.show_button = QPushButton("Show")
        self.show_button.clicked.connect(self.show_invoice)
        layout.addWidget(self.show_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def show_invoice(self):
        """ Fetches and displays invoice details. """
        invoice_no = self.invoice_no_input.text()

        if not invoice_no.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid invoice number!")
            return

        result, error = get_invoice(int(invoice_no))
        if error:
            QMessageBox.critical(self, "Error", error)
            return

        if not result:
            QMessageBox.information(self, "No Data", "No invoice found with the given number.")
            return

        details = "\n".join([f"Date: {result[0][0]}", f"Invoice No: {result[0][1]}", f"Amount: {result[0][5]}"])
        QMessageBox.information(self, "Invoice Details", details)
