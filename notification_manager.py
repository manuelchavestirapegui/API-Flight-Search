import smtplib
import os

class NotificationManager:

    def __init__(self):
        self.gmail = 'chavesmanu1@gmail.com'
        self.outlook = 'manuchaves95@hotmail.com'
        self.password = os.environ.get("EMAIL_PASSWORD")

    def send_email(self, message):
        connection = smtplib.SMTP('smtp.gmail.com', port=587)
        connection.starttls()
        connection.login(user=self.gmail, password=self.password)
        connection.sendmail(from_addr=self.gmail, to_addrs=self.outlook,
                            msg=message.encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore').decode(
                                'utf-8'))
        connection.close()
