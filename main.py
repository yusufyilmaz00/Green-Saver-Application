from database import DatabaseManager
from gui import GUIManager

if __name__ == "__main__":
    db_manager = DatabaseManager()
    gui_manager = GUIManager()

    db_manager.connect()
    gui_manager.run()
