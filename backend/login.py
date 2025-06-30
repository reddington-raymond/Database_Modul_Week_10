import sys
from PyQt6 import QtWidgets, uic
from preference_menu import PreferenceMenuWindow
from admin_preference_menu import AdminPreferenceMenuWindow
from utils import get_engine
import pandas as pd

class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.pushButton_login.clicked.connect(self.handle_login)  # Giriş butonu
        self.pushButton_exit.clicked.connect(QtWidgets.QApplication.quit)  # Exit butonu
        self.label_status.setText("")  # Uyarı etiketi

    def handle_login(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        try:
            engine = get_engine()
            df = pd.read_sql("SELECT * FROM kullanicilar", engine)
            df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
            user = df[(df['KullaniciAdi'] == username) & (df['Parola'] == password)]
            if not user.empty:
                yetki = user.iloc[0]['Yetki']
                self.label_status.setText("Giriş başarılı!")
                if yetki == "admin":
                    self.open_admin_menu()
                elif yetki == "user":
                    self.open_user_menu()
                else:
                    self.label_status.setText("Yetki tanımsız!")
            else:
                self.label_status.setText("Kullanıcı adı veya şifre yanlış!")
        except Exception as e:
            self.label_status.setText(f"Hata: {e}")

    def open_admin_menu(self):
        self.admin_menu = AdminPreferenceMenuWindow()
        self.admin_menu.show()
        self.close()

    def open_user_menu(self):
        self.user_menu = PreferenceMenuWindow()
        self.user_menu.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())