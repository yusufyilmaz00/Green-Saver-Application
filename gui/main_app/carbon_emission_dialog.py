from PyQt5.QtWidgets import QDialog, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHeaderView
from database.operations import calculate_carbon_emission

class CarbonEmissionDialog(QDialog):
    def __init__(self, subscription_no):
        super().__init__()

        self.setWindowTitle("Carbon Emission")
        self.setGeometry(200, 200, 600, 400)

        self.subscription_no = subscription_no

        layout = QVBoxLayout()

        label = QLabel("Your Carbon Emissions:")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Invoice No", "Carbon Emission (kg)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_table()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def populate_table(self):
        result, error = calculate_carbon_emission(self.subscription_no)
        if error:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Error"))
            self.table.setItem(0, 1, QTableWidgetItem(error))
            return

        self.table.setRowCount(len(result))
        for row_idx, (invoice_no, carbon_emission) in enumerate(result):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(invoice_no)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{carbon_emission:.2f}"))
