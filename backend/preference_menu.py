from PyQt6 import QtWidgets, uic, QtGui
from applications_menu import ApplicationsWindow
from interviews_menu import InterviewsMenuWindow
from mentor_menu import MentorMeetingWindow


class PreferenceMenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/preference_menu.ui", self)
        self.pushButton_application.clicked.connect(self.open_applications_window)  # <-- EKLENDİ
        self.pushButton_interviews.clicked.connect(self.open_interviews_window)  # <-- EKLENDİ
        self.pushButton_mentormeeting.clicked.connect(self.open_mentor_meeting_window)
        self.pushButton_exit.clicked.connect(self.close)
        
        self.label_language.setFont(QtGui.QFont("Arial", 4))
        
    def open_applications_window(self):
        self.applications_window = ApplicationsWindow(parent=self)  # parent=self ile pencereyi bağla
        self.applications_window.show()
        self.hide()

    def open_interviews_window(self):
        self.interviews_window = InterviewsMenuWindow(parent=self)  # parent=self ile pencereyi bağla
        self.interviews_window.show()
        self.hide()
        
    def open_mentor_meeting_window(self):
        self.mentor_meeting_window = MentorMeetingWindow(parent=self)  # parent=self ile pencereyi bağla
        self.mentor_meeting_window.show()
        self.hide()

# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = PreferenceMenuWindow()
    window.show()
    sys.exit(app.exec())