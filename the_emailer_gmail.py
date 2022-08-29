import os.path
import base64
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.modify']


def send_email(to_email, the_subject, the_message):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message.set_content(the_message)
    message['To'] = to_email
    message['From'] = 'j.naeder@sae.edu'
    message['Subject'] = the_subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    service.users().messages().send(userId="me", body=create_message).execute()


def send_missed_booking_email(student_object, booking_info):
    student_name = student_object.get_first_name()
    student_email = "madhead324@gmail.com"
    booked_room = booking_info.__getattribute__("res_name")
    booking_start_time = datetime.datetime.fromisoformat(booking_info.__getattribute__("start")).strftime(
        "%m/%d at %I:%M %p")

    the_subject = f"Missed {booked_room} Booking - {booking_start_time}"
    with open("Email Templates/missed_booking.txt", "r") as the_file:
        new_message = the_file.read() % (student_name, booked_room, booking_start_time)
    send_email(student_email, the_subject, new_message)


def send_not_allowed_graduate_booking(student_object, booking_info):
    student_name = student_object.get_first_name()
    student_email = "madhead324@gmail.com"
    booked_room = booking_info.__getattribute__("res_name")
    booking_start_time = datetime.datetime.fromisoformat(booking_info.__getattribute__("start")).strftime(
        "%m/%d at %I:%M %p")

    the_subject = f"Deleted {booked_room} Booking - {booking_start_time}"
    with open("Email Templates/not_allowed_graduate_booking.txt", "r") as the_file:
        new_message = the_file.read() % (student_name, booked_room, booking_start_time)
    send_email(student_email, the_subject, new_message)


def send_not_allowed_mod_booking(student_object, booking_info, allowed_mod):
    student_name = student_object.get_first_name()
    student_email = "j.naeder324@gmail.com"
    student_mod = student_object.get_mod()
    booked_room = booking_info.__getattribute__("res_name")
    booking_start_time = datetime.datetime.fromisoformat(booking_info.__getattribute__("start")).strftime(
        "%m/%d at %I:%M %p")

    the_subject = f"Deleted {booked_room} Booking - {booking_start_time}"
    with open("Email Templates/not_allowed_mod_booking.txt", "r") as the_file:
        new_message = the_file.read() % (student_name, booked_room, booking_start_time, student_mod, booked_room, allowed_mod)
    send_email(student_email, the_subject, new_message)
