from PyQt6 import QtWidgets, uic
import pandas as pd
from utils import get_engine

class MentorMeetingWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_menu = parent
        uic.loadUi("ui/mentor_menu.ui", self)
        self.df = None
        self.load_table_data()
        self.pushButton_AllApplication.clicked.connect(self.show_applications)
        self.pushButton_search.clicked.connect(self.search_applications)
        self.comboBox_secenekler.currentIndexChanged.connect(self.listComboBoxChanged)
        self.pushButton_backmenu.clicked.connect(self.back_to_menu)
        self.pushButton_exit.clicked.connect(self.close)
        self.comboBox_secenekler.addItems([
            "VIT projesinin tamamına katılması uygun olur",
            "VIT projesi ilk IT eğitimi alıp ITPH a yönlendirilmesi uygun olur",
            "VIT projesi ingilizce eğitimi alıp ITPH a yönlendirilmesi uygun olur",
            "VIT projesi kapsamında direkt ITPH a yönlendirilmesi uygun olur.",
            "Direkt bireysel koçluk ile işe yönlendirilmesi uygun olur",
            "Bir sonraki VIT projesine katilmasi daha uygun olur",
            "Başka bir sektöre yönlendirilmeli",
            "Diger"
        ])
        self.comboBox_secenekler.setCurrentIndex(0)
        self.comboBox_secenekler.setEditable(True)
        self.comboBox_secenekler.lineEdit().setPlaceholderText("Sonuç Seçiniz")
        self.comboBox_secenekler.lineEdit().setReadOnly(False)

    def get_base_query(self):
        return """
            SELECT 
                m."GorusmeTarihi" AS "Date",
                b."BasvuruDonemi" AS "Group",
                k."AdSoyad" AS "Full Name",
                m."Mentoradsoyad" AS "Mentor",
                m."VITProjesineKatilabilirMi" AS "Mentor Advice",
                m."Dusunce" AS "Note"
            FROM mentorgorusme m
            LEFT JOIN kursiyerler k ON m."KursiyerID" = k."KursiyerID"
            LEFT JOIN basvurular b ON m."KursiyerID" = b."KursiyerID"
        """

    def load_table_data(self):
        try:
            engine = get_engine()
            query = self.get_base_query()
            self.df = pd.read_sql(query, engine)
            self.show_table(self.df)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")

    def show_table(self, df):
        self.tableWidget_mentor_menu_dashboard.setRowCount(len(df))
        self.tableWidget_mentor_menu_dashboard.setColumnCount(len(df.columns))
        self.tableWidget_mentor_menu_dashboard.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                self.tableWidget_mentor_menu_dashboard.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def show_applications(self):
        self.load_table_data()

    def search_applications(self):
        search_text = self.lineEdit_search.text().lower()
        if search_text == "":
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen arama metni girin.")
            return
        filtered_df = self.df[self.df["Full Name"].str.lower().str.contains(search_text)]
        if filtered_df.empty:
            QtWidgets.QMessageBox.information(self, "Sonuç", "Arama kriterlerine uygun başvuru bulunamadı.")
        else:
            self.show_table(filtered_df)

    def listComboBoxChanged(self):
        selected_option = self.comboBox_secenekler.currentText()
        filtered_df = self.df[self.df['Mentor Advice'] == selected_option]
        if filtered_df.empty:
            QtWidgets.QMessageBox.information(self, "Sonuç", "Seçilen kritere uygun başvuru bulunamadı.")
        else:
            self.show_table(filtered_df)
            QtWidgets.QMessageBox.information(self, "Sonuç", f"{len(filtered_df)} başvuru bulundu.")

    def back_to_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()

# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MentorMeetingWindow()
    window.show()
    sys.exit(app.exec())