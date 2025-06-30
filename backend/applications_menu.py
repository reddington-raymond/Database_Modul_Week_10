from PyQt6 import QtWidgets, uic
import pandas as pd
from utils import get_engine

class ApplicationsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_menu = parent
        uic.loadUi("ui/applications_menu.ui", self)
        self.df = None
        self.load_table_data()
        self.lineEdit_search.textChanged.connect(self.filter_table)
        self.pushButton_all_applications.clicked.connect(self.load_table_data)
        self.pushButton_planned_mentor_meetings.clicked.connect(self.planned_mentor_meetings)
        self.pushButton_unscheduled_mentor_meetings.clicked.connect(self.unscheduled_mentor_meetings)
        self.pushButton_repeted_registeration.clicked.connect(self.repeated_registration)
        self.pushButton_dif_registeration.clicked.connect(self.different_registration)
        self.pushButton_filter_application.clicked.connect(self.filter_applications)
        self.pushButton_BackMenu.clicked.connect(self.back_to_menu)
        self.pushButton_exit.clicked.connect(self.close)

    def get_base_query(self):
        return """
            
        SELECT 
            "ZamanDamgasi" AS Date,
            "AdSoyad" AS Name_Surname,
            "MailAdresi" AS Mail,
            "TelefonNumarasi" AS Telephone,
            "PostaKodu" AS Post_Code,
            "YasadiginizEyalet" AS State,
            "EkonomikDurum" AS Economical_Situation,
            "MentorGorusmesi" AS MentorMeeting         
            FROM basvurular
            JOIN Kursiyerler ON Kursiyerler."KursiyerID" = basvurular."KursiyerID" 

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
        self.tableWidget_application_dashboard.setRowCount(len(df))
        self.tableWidget_application_dashboard.setColumnCount(len(df.columns))  
        self.tableWidget_application_dashboard.setHorizontalHeaderLabels(
            ["Date", "Name Surname", "Mail", "Telephone", "Post Code", "State", "Economical Situation", "Mentor Meeting"]
        )
        for row in range(len(df)):
            for col in range(8):  # Sadece ilk 7 sütunu göster
                value = str(df.iloc[row, col])
                self.tableWidget_application_dashboard.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def filter_table(self):
        if self.df is None:
            return
        try:
            search_text = self.lineEdit_search.text().lower()
            if search_text == "":
                filtered_df = self.df
            else:
                filtered_df = self.df[self.df['Name Surname'].str.lower().str.contains(search_text, na=False)]
                
            return self.show_table(filtered_df)
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Arama hatası: {e}")

    def planned_mentor_meetings(self):
        if self.df is None:
            self.load_table_data()
        try:
            if "MentorMeeting" in self.df.columns:
                # Mentor görüşmesi planlanmış olanları filtrele
                filtered = self.df[self.df["MentorMeeting"] != "planlanmadı"]
            else:
                QtWidgets.QMessageBox.warning(self, "Uyarı", "MentorGorusmesi sütunu bulunamadı!")
                return
            self.show_table(filtered)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Filtreleme hatası: {e}")

    def unscheduled_mentor_meetings(self):
        if self.df is None:
            self.load_table_data()
        try:
            if "MentorMeeting" in self.df.columns:
                # Henüz mentor görüşmesi planlanmamış olanları filtrele
                filtered = self.df[self.df["MentorMeeting"] == "planlanmadı"]
            else:
                QtWidgets.QMessageBox.warning(self, "Uyarı", "MentorGorusmesi sütunu bulunamadı!")
                return
            self.show_table(filtered)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Filtreleme hatası: {e}")

    def repeated_registration(self):
        if self.df is None:
            self.load_table_data()
        try:
            required_columns = ["Name_Surname", "Mail"]
            if all(col in self.df.columns for col in required_columns):
                filtered = self.df[self.df.duplicated(subset=required_columns, keep=False)]
            else:
                missing_cols = [col for col in required_columns if col not in self.df.columns]
                QtWidgets.QMessageBox.warning(self, "Uyarı", f"Gerekli sütunlar bulunamadı: {missing_cols}")
                return
            self.show_table(filtered)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Tekrarlanan kayıt filtreleme hatası: {e}")

    def different_registration(self):
        if self.df is None:
            self.load_table_data()
        try:
            required_columns = ["Name_Surname", "Mail"]
            if all(col in self.df.columns for col in required_columns):
                # Farklı kayıtlar: Aynı isim ve mail başka bir yerde yoksa
                merged = self.df.groupby(required_columns).size().reset_index(name='counts')
                unique = merged[merged['counts'] == 1]
                filtered = self.df.set_index(required_columns).loc[unique.set_index(required_columns).index].reset_index()
            else:
                missing_cols = [col for col in required_columns if col not in self.df.columns]
                QtWidgets.QMessageBox.warning(self, "Uyarı", f"Gerekli sütunlar bulunamadı: {missing_cols}")
                return
            self.show_table(filtered)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Farklı kayıt filtreleme hatası: {e}")

    def filter_applications(self):
        if self.df is None:
            self.load_table_data()
        try:
            required_columns = ["Name_Surname", "Mail"]
            if all(col in self.df.columns for col in required_columns):
                filtered = self.df.drop_duplicates(subset=required_columns)
            else:
                missing_cols = [col for col in required_columns if col not in self.df.columns]
                QtWidgets.QMessageBox.warning(self, "Uyarı", f"Gerekli sütunlar bulunamadı: {missing_cols}")
                return
            self.show_table(filtered)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Başvuru filtreleme hatası: {e}")

    def back_to_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()

# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationsWindow()
    window.show()
    sys.exit(app.exec())