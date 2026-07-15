# Test deneme 
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
 
def main():
    # Programı başlatan ana nesne
    app = QApplication(sys.argv)
    
    # Arayüz penceresini oluştur ve ekranda göster
    window = MainWindow()
    window.show()
    
    # Program kapatılana kadar çalışmaya devam etmesini sağla
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    main()
