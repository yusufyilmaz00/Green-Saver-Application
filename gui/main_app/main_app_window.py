from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from gui.main_app.carbon_emission_dialog import CarbonEmissionDialog
from gui.main_app.compare_invoices_dialog import CompareInvoicesDialog
from gui.main_app.compare_all_time_invoices_dialog import CompareAllTimeInvoicesDialog  # Yeni eklenen dialog
from gui.main_app.show_all_invoices_dialog import ShowAllInvoicesDialog
from gui.main_app.add_invoice_dialog import AddInvoiceDialog
from gui.main_app.delete_invoice_dialog import DeleteInvoiceDialog
from gui.main_app.update_invoice_dialog import UpdateInvoiceDialog
from gui.main_app.show_invoice_dialog import ShowInvoiceDialog

class MainAppWindow(QWidget):
    def __init__(self, user_info, subscription_no, subscriber_type):
        super().__init__()

        self.subscription_no = subscription_no
        self.subscriber_type = subscriber_type

        self.setWindowTitle("Main Application")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        # Welcome message
        welcome_label = QLabel(f"Welcome, {user_info}")
        welcome_label.setStyleSheet("color: blue; font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(welcome_label)

        # Invoice buttons
        self.add_invoice_button = QPushButton("Add Invoice")
        self.add_invoice_button.clicked.connect(self.open_add_invoice_window)
        layout.addWidget(self.add_invoice_button)

        self.delete_invoice_button = QPushButton("Delete Invoice")
        self.delete_invoice_button.clicked.connect(self.open_delete_invoice_window)
        layout.addWidget(self.delete_invoice_button)

        self.update_invoice_button = QPushButton("Update Invoice")
        self.update_invoice_button.clicked.connect(self.open_update_invoice_window)
        layout.addWidget(self.update_invoice_button)

        self.show_invoice_button = QPushButton("Show Invoice")
        self.show_invoice_button.clicked.connect(self.open_show_invoice_window)
        layout.addWidget(self.show_invoice_button)

        # Carbon Emission Button
        self.carbon_button = QPushButton("Calculate Carbon Emission")
        self.carbon_button.clicked.connect(self.open_carbon_emission_window)
        layout.addWidget(self.carbon_button)

        # Compare Invoices Button
        self.compare_button = QPushButton("Compare Monthly Invoices")
        self.compare_button.clicked.connect(self.open_compare_invoices_window)
        layout.addWidget(self.compare_button)

        # Compare All-Time Invoices Button (Yeni Buton)
        self.compare_all_time_button = QPushButton("Compare All-Time Invoices")
        self.compare_all_time_button.clicked.connect(self.open_compare_all_time_invoices_window)
        layout.addWidget(self.compare_all_time_button)

        # Show All Invoices Button
        self.show_invoices_button = QPushButton("Show My All Invoices")
        self.show_invoices_button.clicked.connect(self.show_all_invoices_window)
        layout.addWidget(self.show_invoices_button)

        # Logout Button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def open_add_invoice_window(self):
        dialog = AddInvoiceDialog(self.subscription_no, self.subscriber_type)
        dialog.exec_()

    def open_delete_invoice_window(self):
        dialog = DeleteInvoiceDialog(self.subscription_no)
        dialog.exec_()

    def open_update_invoice_window(self):
        dialog = UpdateInvoiceDialog(self.subscription_no, self.subscriber_type)
        dialog.exec_()

    def open_show_invoice_window(self):
        dialog = ShowInvoiceDialog()
        dialog.exec_()

    def open_carbon_emission_window(self):
        dialog = CarbonEmissionDialog(self.subscription_no)
        dialog.exec_()

    def open_compare_invoices_window(self):
        dialog = CompareInvoicesDialog(self.subscription_no)
        dialog.exec_()

    def open_compare_all_time_invoices_window(self):
        """ Opens the compare all-time invoices dialog. """
        dialog = CompareAllTimeInvoicesDialog(self.subscription_no)
        dialog.exec_()

    def show_all_invoices_window(self):
        dialog = ShowAllInvoicesDialog(self.subscription_no)
        dialog.exec_()

    def logout(self):
        """ Logs out the user and closes the window. """
        self.close()
