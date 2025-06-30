from PyQt6 import QtWidgets, uic
import pandas as pd
from utils import get_engine

class InterviewsMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_menu = parent
        uic.loadUi("ui/interviews_menu.ui", self)
        self.df = None
        self.load_table_data()
        self.lineEdit_search.textChanged.connect(self.filter_table)
        self.pushButton_all_submitted_projects.clicked.connect(self.show_submitted_projects)
        self.pushButton_project_arrivals.clicked.connect(self.show_project_arrivals)
        self.pushButton_BackMenu.clicked.connect(self.back_to_menu)
        self.pushButton_exit.clicked.connect(self.close)

    def get_base_query(self):
        return """
            SELECT 
                k."AdSoyad" AS "Name Surname",
                p."ProjeGonderilisTarihi" AS "Project Sending Date",
                p."ProjeninGelisTarihi" AS "Project Arrival Date"
            FROM projetakip p
            LEFT JOIN kursiyerler k
              ON p."KursiyerID" = k."KursiyerID"
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
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def filter_table(self):
        if self.df is None:
            return
        search_text = self.lineEdit_search.text().lower()
        if search_text == "":
            filtered_df = self.df
        else:
            filtered_df = self.df[self.df['Name Surname'].str.lower().str.contains(search_text)]
        self.show_table(filtered_df)

    def show_submitted_projects(self):
        if self.df is None:
            self.load_table_data()
        filtered = self.df[self.df["Project Sending Date"].notnull()]
        self.show_table(filtered)

    def show_project_arrivals(self):
        if self.df is None:
            self.load_table_data()
        filtered = self.df[self.df["Project Arrival Date"].notnull()]
        self.show_table(filtered)

    def back_to_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()

# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = InterviewsMenuWindow()
    window.show()
    sys.exit(app.exec())