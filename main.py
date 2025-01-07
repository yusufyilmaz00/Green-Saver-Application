import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui import MainWindow  # GUI modülü
from database import DatabaseManager  # Veritabanı bağlantı sınıfı

def main():
    # Veritabanı bağlantısını başlat
    db_manager = DatabaseManager()
    connection = db_manager.create_connection()

    if not connection:
        # Bağlantı başarısızsa hata mesajı göster ve çık
        print("Failed to connect to the database!")
        QMessageBox.critical(
            None, 
            "Database Error", 
            "Could not connect to the database. Please check your configuration."
        )
        sys.exit(1)

    print("Database connection established successfully.")

    # PyQt5 uygulamasını başlat
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # Olay döngüsünü çalıştır
    exit_code = app.exec_()

    # Uygulama kapandığında veritabanı bağlantısını kapat
    db_manager.close_connection()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
