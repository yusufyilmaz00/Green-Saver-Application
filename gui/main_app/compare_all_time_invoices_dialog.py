from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from database.operations import compare_all_time_average_with_message

class CompareAllTimeInvoicesDialog(QDialog):
    def __init__(self, subscription_no):
        super().__init__()

        self.subscription_no = subscription_no

        self.setWindowTitle("Compare All-Time Invoices")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        # Invoice Type Selection
        self.invoice_type_label = QLabel("Select Invoice Type:")
        self.invoice_type_combo = QComboBox()
        self.invoice_type_combo.addItems(["Electricity", "Natural Gas", "Water"])
        layout.addWidget(self.invoice_type_label)
        layout.addWidget(self.invoice_type_combo)

        # Compare Button
        self.compare_button = QPushButton("Compare")
        self.compare_button.clicked.connect(self.compare_all_time_invoices)
        layout.addWidget(self.compare_button)

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def compare_all_time_invoices(self):
        """ Fetches comparison results and displays recommendation messages. """
        selected_type = self.invoice_type_combo.currentText()

        if not selected_type:
            QMessageBox.warning(self, "Warning", "Please select an invoice type.")
            return

        # Fetch recommendation
        _, message, error = compare_all_time_average_with_message(self.subscription_no, selected_type)

        if error:
            QMessageBox.critical(self, "Error", error)
        elif message is None:
            QMessageBox.information(self, "No Data", "No invoices found for the selected type.")
        else:
            QMessageBox.information(self, "Recommendation", message)

        self.close()
