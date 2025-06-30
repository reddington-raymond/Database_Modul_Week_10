from PyQt6 import QtWidgets, uic
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv  # .env dosyasını okumak için
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# .env dosyasını yükle
load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "../token.json")

class AdminMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_menu = parent
        uic.loadUi("ui/admin_menu.ui", self)
        self.pushButton_preference_admin_menu.clicked.connect(self.back_to_admin_preference_menu)
        self.pushButton_activity_control.clicked.connect(self.load_activities_to_table)
        self.pushButton_sendmail.clicked.connect(self.send_emails_to_participants)
        self.pushButton_exit.clicked.connect(QtWidgets.QApplication.quit)

    def back_to_admin_preference_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()

    def get_calendar_service(self):
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                from google_auth_oauthlib.flow import InstalledAppFlow
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    def load_activities_to_table(self):
        service = self.get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=20, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        table = self.tableWidget_admin_menu_dashboard
        table.setRowCount(len(events))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Event Name", "Start Time", "Organizer Email", "Participants"])

        for row, event in enumerate(events):
            event_name = event.get('summary', 'No Title')
            start_time = event['start'].get('dateTime', event['start'].get('date', ''))
            organizer_email = event.get('organizer', {}).get('email', '')
            participants = [att.get('email', '') for att in event.get('attendees', [])] if 'attendees' in event else []
            participants_str = ", ".join(participants)

            table.setItem(row, 0, QtWidgets.QTableWidgetItem(event_name))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(start_time))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(organizer_email))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(participants_str))

    def send_emails_to_participants(self):
        service = self.get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=20, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        sender_email = "vit7team2crmproject@gmail.com"
        # .env dosyasından şifreyi oku
        sender_password = os.environ.get("CRM_GMAIL_APP_PASSWORD")

        if not sender_password:
            QtWidgets.QMessageBox.critical(self, "Hata", "Mail gönderimi için uygulama şifresi bulunamadı!")
            return

        for event in events:
            event_name = event.get('summary', 'No Title')
            start_time = event['start'].get('dateTime', event['start'].get('date', ''))
            participants = [att.get('email', '') for att in event.get('attendees', [])] if 'attendees' in event else []

            for recipient in participants:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = f"Etkinlik Daveti: {event_name}"

                body = f"Merhaba,\n\n{event_name} etkinliğine davetlisiniz.\nBaşlangıç Zamanı: {start_time}\n\nİyi günler!"
                msg.attach(MIMEText(body, 'plain'))

                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, recipient, msg.as_string())
                    print(f"Mail gönderildi: {recipient}")
                except Exception as e:
                    print(f"Mail gönderilemedi: {recipient}, Hata: {e}")

        QtWidgets.QMessageBox.information(self, "Bilgi", "Tüm katılımcılara mail gönderimi tamamlandı.")

# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AdminMenuWindow()
    window.show()
    sys.exit(app.exec())