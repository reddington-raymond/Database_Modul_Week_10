from PyQt6 import QtWidgets, uic
from applications_menu import ApplicationsWindow
from interviews_menu import InterviewsMenuWindow
from mentor_menu import MentorMeetingWindow
from adminmenu import AdminMenuWindow

class AdminPreferenceMenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/admin_preference_menu.ui", self)
        self.pushButton_mentorinterview.clicked.connect(self.open_mentor_interviews_window)
        self.pushButton_applications.clicked.connect(self.open_applications_window)
        self.pushButton_interviews.clicked.connect(self.open_interviews_window)
        self.pushButton_adminmenu.clicked.connect(self.open_admin_menu_window)
        self.pushButton_exit.clicked.connect(self.close)
    
    def open_mentor_interviews_window(self):
        self.interviews_window = MentorMeetingWindow(parent=self)
        self.interviews_window.show()
        self.hide()
       
    def open_applications_window(self):
        self.applications_window = ApplicationsWindow(parent=self)
        self.applications_window.show()
        self.hide()
     
    def open_interviews_window(self):
        self.interviews_window = InterviewsMenuWindow(parent=self)
        self.interviews_window.show()
        self.hide()
        
    def open_admin_menu_window(self):
        self.admin_menu_window = AdminMenuWindow(parent=self)
        self.admin_menu_window.show()
        self.hide()
        
   
        
# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AdminPreferenceMenuWindow()
    window.show()
    sys.exit(app.exec())