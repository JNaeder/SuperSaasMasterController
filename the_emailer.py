import smtplib
from email.mime.text import MIMEText


class Emailer:
    def __init__(self):
        self.sender_email = "ny_tech@sae.edu"
        self.sender_password = "Jenny#867"

    def send_email(self, recipient_email, subject, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.sender_email, self.sender_password)
        final_message = MIMEText(f"Subject: {subject}\n\n {message}")
        server.sendmail(self.sender_email, recipient_email, final_message)
        server.quit()


if __name__ == "__main__":
    emailer = Emailer()
    emailer.send_email("Madhead324@gmail.com", "This is just a test", "TEEEESSSSSSTTTT")

