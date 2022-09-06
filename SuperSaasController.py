from SuperSaaS import Client, Configuration
import the_emailer_gmail
from mysql.connector.locales.eng import client_error
import mysql.connector
from mysql.connector.errors import *
# import gspread
import datetime
import json
from add_bookings_repeating import TeacherBooking
import sys
import os


class StudentClass:
    def __init__(self, student_id, proper_name, icr, gpa, mod, saas_id="", the_credits=""):
        self._student_id = student_id
        self._proper_name = proper_name
        self._icr = icr
        self._gpa = gpa
        self._mod = mod
        self._saas_id = saas_id
        self._credits = the_credits
        self._last_name = ""
        self._first_name = ""
        self.set_full_names()
        self._full_name = f"{self._first_name} {self._last_name}"

    def set_full_names(self):
        split_name = self._proper_name.split(", ")
        if len(split_name) > 1:
            self._last_name = split_name[0]
            self._first_name = split_name[1]
        else:
            self._first_name = self._proper_name

    def __repr__(self):
        output = f"{self._full_name} ({self._student_id}) GPA: {self._gpa} ICR: {self._icr} {self._mod}" \
                 f" saas_id: {self._saas_id} "
        return output

    def get_student_id(self):
        return self._student_id

    def get_full_name(self):
        return self._full_name

    def get_proper_name(self):
        return self._proper_name

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_icr(self):
        return self._icr

    def get_gpa(self):
        return self._gpa

    def get_mod(self):
        return self._mod

    def set_saas_id(self, saas_id):
        self._saas_id = saas_id

    def get_saas_id(self):
        return self._saas_id

    def set_credits(self, new_credits):
        self._credits = new_credits

    def get_credits(self):
        return self._credits


class StudentObjectHolder:
    def __init__(self):
        self._list_of_student_objects = []

    def get_list_of_student_objects(self):
        return self._list_of_student_objects

    def reset_list_of_student(self):
        self._list_of_student_objects = []

    def add_student(self, the_student_object):
        self._list_of_student_objects.append(the_student_object)

    def add_parameter_by_id(self, student_id, parameter):
        student = self.get_student_by_student_id(student_id)
        if student is not None:
            student.set_saas_id(parameter)

    def get_student_by_student_id(self, student_id):
        for student in self._list_of_student_objects:
            if student.get_student_id() == student_id:
                return student
        return None


class DatabaseInfo:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="192.168.133.4",
            port="3306",
            user="nytech",
            password="Jenny#867",
            database="SAE_NYC"
        )
        self.cursor = self.database.cursor()

    def reset_db(self):
        self.database.commit()

    def get_mod_from_studio_name(self, studio_name):
        sql = f"SELECT mod_section FROM studio_info WHERE studio_name='{studio_name}'"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def get_student_info_from_student_id(self, student_id):
        try:
            sql = f"SELECT * FROM all_active WHERE student_id={student_id}"
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except ProgrammingError:
            return None

    def get_grad_info_from_student_id(self, student_id):
        try:
            sql = f"SELECT * FROM grads WHERE student_id={student_id}"
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except ProgrammingError:
            return None

    def get_student_object_from_id(self, student_id, the_name="", email_end=""):
        student_info = self.get_student_info_from_student_id(student_id)
        grad_info = self.get_grad_info_from_student_id(student_id)
        if student_info is not None:
            proper_name = student_info[1]
            icr = student_info[3]
            gpa = student_info[4]
            mod = "Mod " + str(student_info[2][4])
            new_student = StudentClass(student_id, proper_name, icr, gpa, mod)
            return new_student
        elif grad_info is not None:
            proper_name = grad_info[0]
            icr = "-"
            gpa = "-"
            mod = "Graduate"
            new_student = StudentClass(student_id, proper_name, icr, gpa, mod)
            return new_student
        elif email_end != "sae.edu":
            name_split = the_name.split(" ")
            if len(name_split) >= 2:
                proper_name = f"{the_name.split(' ')[1]}, {the_name.split(' ')[0]}"
            else:
                proper_name = the_name
            new_student = StudentClass(student_id, proper_name, 0, 0, "NOT ACTIVE", "-")
            return new_student

    def get_blocked_student_ids(self):
        sql = f"SELECT student_id FROM block_list"
        self.cursor.execute(sql)
        output = [x[0] for x in self.cursor.fetchall()]
        return output

    def get_blocked_info(self, student_id):
        sql = f"SELECT * FROM block_list WHERE student_id={student_id}"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def add_student_to_block_list(self, student_id, proper_name, the_date):
        blocked_ids = self.get_blocked_student_ids()
        if int(student_id) not in blocked_ids:
            sql_2 = f"INSERT INTO block_list (student_id, student_name, blocked_date) " \
                    f"VALUES({student_id}, '{proper_name}', '{the_date}')"
            self.cursor.execute(sql_2)
            self.database.commit()

    def remove_student_from_block_list(self, student_id):
        sql = f"DELETE FROM block_list WHERE student_id={student_id}"
        self.cursor.execute(sql)
        self.database.commit()

    def get_today_booking_ids(self):
        sql = f"SELECT booking_id FROM today_bookings"
        self.cursor.execute(sql)
        output = [x[0] for x in self.cursor.fetchall()]
        return output

    def get_all_today_bookings(self):
        sql = f"SELECT * FROM today_bookings"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def set_today_bookings(self, bookings_list):
        for booking in bookings_list:
            booking_email_ending = booking.__getattribute__("created_by").split(" ")[0].split("@")[1]
            booking_id = booking.__getattribute__("id")
            studio_name = booking.__getattribute__("res_name")
            booking_time = datetime.datetime.fromisoformat(booking.__getattribute__("start"))
            student_name = booking.__getattribute__("full_name")

            if booking_id not in self.get_today_booking_ids() and booking_email_ending != "sae.edu":
                sql_1 = f"INSERT INTO today_bookings (booking_id, studio_name, booking_datetime, student_name) " \
                        f"VALUES ({booking_id}, '{studio_name}', '{booking_time.isoformat()}', '{student_name}')"
                self.cursor.execute(sql_1)
                self.database.commit()

        for db_booking in self.get_all_today_bookings():
            booking_id = db_booking[0]
            booking_time = db_booking[2]
            booking_day = booking_time.date()

            if booking_day != datetime.datetime.today().date():
                sql_2 = f"DELETE FROM today_bookings WHERE booking_id={booking_id}"
                self.cursor.execute(sql_2)
                self.database.commit()

    def get_booking_status_by_booking_id(self, booking_id):
        sql = f"SELECT status FROM today_bookings WHERE booking_id={booking_id}"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def set_booking_status_by_booking_id(self, booking_id, new_status):
        sql = f"UPDATE today_bookings SET status='{new_status}' WHERE booking_id={booking_id}"
        self.cursor.execute(sql)
        self.database.commit()

    # def log_to_log_book(self, student_object, the_log):
    #     student_name = student_object.get_full_name()
    #     student_id = student_object.get_student_id()
    #     the_datetime = datetime.datetime.now()
    #     the_date = the_datetime.strftime("%m/%d/%Y")
    #     the_time = the_datetime.strftime("%H:%M:%S")
    #     log_list = [student_name, student_id, the_date, the_time, the_log]
    #     self._log_book.append_row(log_list)


class SuperSaasController:
    def __init__(self):
        self._app = None
        config = Configuration()
        self._client = Client(config)
        self._client.account_name = None
        self._client.api_key = None
        self._schedule_id = None
        self._all_bookings = None
        self._all_users = None
        self._all_employees = None
        self._icr_cutoff = None
        self._gpa_cutoff = None
        self._student_holder = StudentObjectHolder()
        self._database = DatabaseInfo()
        self._teacher_booking = TeacherBooking(self)
        self._number_of_changes = 0

        self.read_json_data()
        self.setup_student_holder()
        self.setup_employee_list()
        self.set_all_bookings()

    def get_database(self):
        return self._database

    def set_app(self, app):
        self._app = app

    def read_json_data(self):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_to_json = os.path.abspath(os.path.join(bundle_dir, 'data.json'))
        with open(path_to_json, "r") as the_file:
            the_data = json.load(the_file)
        self._icr_cutoff = the_data["icr"]
        self._gpa_cutoff = the_data["gpa"]
        self._client.account_name = the_data["account_name"]
        self._client.api_key = the_data["api_key"]
        self._schedule_id = the_data["schedule_id"]

    def get_icr(self):
        return self._icr_cutoff

    def set_icr(self, new_icr):
        self._icr_cutoff = new_icr

    def get_teacher_booking(self):
        return self._teacher_booking

    def get_student_holder(self):
        return self._student_holder

    def set_repeating_bookings(self, the_name, the_mod, the_studio, start_time, end_time, start_date, end_date):
        s_date = [int(date) for date in start_date.split("/")]
        e_date = [int(date) for date in end_date.split("/")]
        s_month, s_day, s_year = s_date
        e_month, e_day, e_year = e_date
        the_start_date = datetime.datetime(s_year, s_month, s_day)
        the_end_date = datetime.datetime(e_year, e_month, e_day)
        list_of_dates = self._teacher_booking.get_list_of_dates_for_term(the_start_date, the_end_date)
        self._teacher_booking.create_repeating_bookings(the_name, the_studio, the_mod, start_time,
                                                        end_time, list_of_dates)

    def get_all_info(self):
        self._database.reset_db()
        self.read_json_data()
        self.setup_student_holder()
        self.setup_employee_list()
        self.set_all_bookings()

    def setup_employee_list(self):
        self._all_users = self._client.users.list(form=False, limit=500)
        output_list = []
        for user in self._all_users:
            email = user.__getattribute__("name").split("@")[1]
            full_name = user.__getattribute__("full_name")
            if email == "sae.edu":
                output_list.append(full_name)
        self._all_employees = output_list

    def get_employee_list(self):
        return self._all_employees

    def setup_student_holder(self):
        self._all_users = self._client.users.list(form=False, limit=500)
        self._student_holder.reset_list_of_student()
        for user in self._all_users:
            student_id = user.__getattribute__("name").split(".")[0]
            supersaas_id = user.__getattribute__("id")
            ss_credit = user.__getattribute__("credit")
            the_name = user.__getattribute__("full_name")
            email_end = user.__getattribute__("name").split("@")[1]
            new_student = self._database.get_student_object_from_id(student_id, the_name, email_end)
            if new_student is not None:
                new_student.set_saas_id(supersaas_id)
                new_student.set_credits(ss_credit)
                self._student_holder.add_student(new_student)

    def set_all_bookings(self):
        date_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        self._all_bookings = self._client.appointments.list(schedule_id=self._schedule_id, limit=1000,
                                                            start_time=date_today)

    def get_bookings_for_today(self):
        day_bookings = self._client.appointments.range(self._schedule_id, True, 100)
        self._database.set_today_bookings(day_bookings)
        return day_bookings

    def get_all_users(self):
        return self._all_users

    def get_number_of_changes(self):
        num_changes = self._number_of_changes
        self._number_of_changes = 0
        return num_changes

    def increase_number_of_changes(self):
        self._number_of_changes += 1

    def create_booking(self, booking_id, attributes):
        self._client.appointments.create(schedule_id=self._schedule_id, user_id=booking_id, attributes=attributes)

    def booking_is_valid(self, student_id, booked_room):
        the_student_object = self._database.get_student_object_from_id(student_id)
        if the_student_object.get_mod() == "Graduate":
            return True
        student_mod = int(the_student_object.get_mod()[-1])
        if booked_room == "Avid S6" and student_mod < 4:
            return False
        if booked_room == "SSL" and student_mod < 3:
            return False
        if booked_room == "Audient" and student_mod < 2:
            return False
        if booked_room == "02R" and student_mod < 2:
            return False
        if "Production Suite" in booked_room and student_mod < 2:
            return False
        return True

    def is_student_blocked(self, student_id):
        return int(student_id) in self._database.get_blocked_student_ids()

    def check_blocked_status(self, student_id):
        the_student_object = self._student_holder.get_student_by_student_id(student_id)
        student_name = the_student_object.get_full_name()
        blocked_data = self._database.get_blocked_info(student_id)
        today_date = datetime.datetime.today().date()
        date_diff = today_date - blocked_data[2]
        if date_diff.days > 7:
            log = f"Removed {student_name} from block list."
            self._app.print_output(log)
            self._database.remove_student_from_block_list(student_id)

    def go_through_all_users(self):
        self.setup_student_holder()
        for user in self._all_users:

            # Get info from SuperSaas about User
            ss_full_name = user.__getattribute__("full_name")
            supersaas_id_num = user.__getattribute__("id")
            ss_credits = user.__getattribute__('credit')
            role = user.__getattribute__('role')
            student_id = user.__getattribute__("name").split(".")[0]
            email_ending = user.__getattribute__("name").split("@")[1]

            # Check if user has an employee email
            if email_ending == "sae.edu" and role != 4:
                new_attributes = {
                    "role": 4,
                    "credit": "-"
                }
                self._client.users.update(supersaas_id_num, new_attributes)
                log = f"Changed {ss_full_name}'s role to Superuser"
                self.increase_number_of_changes()
                self._app.print_output(log)

            # Get student object from ID, and then compare that info with Supersaas info
            the_student_object = self._student_holder.get_student_by_student_id(student_id)

            if the_student_object is not None:
                if self.is_student_blocked(student_id):
                    self.check_blocked_status(student_id)
                else:
                    correct_full_name = the_student_object.get_full_name()
                    student_icr = the_student_object.get_icr()
                    student_gpa = the_student_object.get_gpa()
                    # If the student is listed as a graduate
                    if the_student_object.get_mod() == "Graduate" and ss_credits != "-":
                        log = f"{correct_full_name} is a graduate. Credits set to infinity"
                        self.increase_number_of_changes()
                        self._app.print_output(log)
                        # self._google_sheets.log_to_log_book(the_student_object, log)
                        new_attributes = {
                            "credit": "-"
                        }
                        self._client.users.update(supersaas_id_num, new_attributes)
                        the_student_object.set_credits("-")
                    if the_student_object.get_mod() != "Graduate":
                        can_book = student_icr > self._icr_cutoff and student_gpa >= self._gpa_cutoff
                        # Check if the name of the user is the name in the system
                        if correct_full_name != ss_full_name:
                            new_attributes = {
                                "full_name": correct_full_name
                            }
                            self._client.users.update(supersaas_id_num, new_attributes)
                            log = f"{correct_full_name}'s name has been updated in Student Management." \
                                  f" (OLD NAME: {ss_full_name})"
                            self.increase_number_of_changes()
                            self._app.print_output(log)
                            # self._google_sheets.log_to_log_book(the_student_object, log)

                        # Check if user's credits need to change based on if they can book or not.
                        if ss_credits != "-" and can_book:
                            log = f"{correct_full_name} is now able to book. Credits updated to infinity"
                            self.increase_number_of_changes()
                            self._app.print_output(log)
                            # self._google_sheets.log_to_log_book(the_student_object, log)
                            new_attributes = {
                                "credit": "-"
                            }
                            self._client.users.update(supersaas_id_num, new_attributes)
                            the_student_object.set_credits("-")
                        if ss_credits != "0" and not can_book:
                            if student_icr < self._icr_cutoff:
                                log = f"{correct_full_name} is now below the {self._icr_cutoff}% " \
                                      f"ICR cutoff. Credits have been set to 0"
                            else:
                                log = f"{correct_full_name} is now below the {self._gpa_cutoff} " \
                                      f"GPA cutoff. Credits have been set to 0"
                            self.increase_number_of_changes()
                            self._app.print_output(log)
                            # self._google_sheets.log_to_log_book(the_student_object, log)
                            new_attributes = {
                                "credit": "0"
                            }
                            self._client.users.update(supersaas_id_num, new_attributes)
                            the_student_object.set_credits("0")

            # Check if user is not in the academic system, or not an employee
            elif email_ending != "sae.edu" and ss_credits != "0":
                new_attributes = {
                    "credit": "0"
                }
                self._client.users.update(supersaas_id_num, new_attributes)
                the_student_object.set_credits("0")
                full_name = user.__getattribute__("full_name")
                log = f"{full_name}'s data is not in the system - credits set to 0"
                self.increase_number_of_changes()
                self._app.print_output(log)

    def go_through_all_bookings(self):
        self.set_all_bookings()
        for booking in self._all_bookings:
            student_name = booking.__getattribute__("full_name")
            booked_room = booking.__getattribute__("res_name")
            booking_start_time = booking.__getattribute__("start")
            mod = booking.__getattribute__("field_1_r")
            booking_id = booking.__getattribute__("id")
            student_id = booking.__getattribute__("created_by").split(".")[0]
            the_student_object = self._student_holder.get_student_by_student_id(student_id)
            booking_day = datetime.datetime.fromisoformat(booking.__getattribute__("start")).strftime("%A")
            # If student object exists
            if the_student_object is not None:
                correct_mod = the_student_object.get_mod()
                correct_name = the_student_object.get_full_name()
                correct_student_id = the_student_object.get_student_id()

                # Checks to see if student is allowed to make the booking. Only displays warning message.
                if not self.booking_is_valid(student_id, booked_room):
                    booking_time = datetime.datetime.fromisoformat(booking_start_time)
                    log = f"***BOOKING NOT ALLOWED***: {correct_name} in {correct_mod} booked the {booked_room} " \
                          f"on {booking_time.strftime('%A %m/%d at %H:%M')}"
                    self._app.print_output(log)
                    self.remove_booking_by_booking_id(booking_id)
                    allowed_mod = self._database.get_mod_from_studio_name(booked_room)
                    the_emailer_gmail.send_not_allowed_mod_booking(the_student_object, booking, allowed_mod)

                # Checks to see if graduate is only booking on a Friday. Only displays warning message.
                if correct_mod == "Graduate" and booking_day != "Friday":
                    log = f"***BOOKING NOT ALLOWED***: {correct_name} who is a {correct_mod} " \
                          f"is only allowed to book on Friday. Booking Deleted."
                    self._app.print_output(log)
                    self.remove_booking_by_booking_id(booking_id)
                    the_emailer_gmail.send_not_allowed_graduate_booking(the_student_object, booking)

                # Runs when the name of the booking doesn't match the name in the system
                if correct_name != student_name:
                    attributes = {
                        "full_name": correct_name,
                        "name": correct_student_id + ".us@saeinstitute.edu"
                    }
                    self._client.appointments.update(self._schedule_id, booking_id, attributes)
                    booking_time = datetime.datetime.fromisoformat(booking_start_time)
                    log = f"{correct_name}'s name has been updated for {booked_room} booking for " \
                          f"{booking_time.strftime('%A %m/%d')}. (OLD NAME: {student_name}) "
                    self.increase_number_of_changes()
                    self._app.print_output(log)
                    # self._google_sheets.log_to_log_book(the_student_object, log)

                # Runs when the mod of the booking doesn't match the mod in the system
                if correct_mod != mod:
                    attributes = {
                        "field_1_r": correct_mod,
                        "name": correct_student_id + ".us@saeinstitute.edu"
                    }
                    self._client.appointments.update(self._schedule_id, booking_id, attributes)
                    booking_time = datetime.datetime.fromisoformat(booking_start_time)
                    log = f"{correct_name}'s Mod has been updated for {booked_room} booking for " \
                          f"{booking_time.strftime('%A %m/%d')}"
                    self.increase_number_of_changes()
                    self._app.print_output(log)
                    # self._google_sheets.log_to_log_book(the_student_object, log)

    def get_list_of_bookings_from_agenda(self, supersaas_id):
        output = []
        data = self._client.appointments.agenda(self._schedule_id, supersaas_id)
        today_date = datetime.datetime.today().date()
        for booking in data:
            the_booking_date = datetime.datetime.fromisoformat(booking.__getattribute__("start")).date()
            if the_booking_date > today_date:
                output.append(booking)
        return output

    def remove_booking_by_booking_id(self, booking_id):
        self._client.appointments.delete(self._schedule_id, booking_id)

    def remove_bookings_from_list(self, list_of_bookings):
        for booking in list_of_bookings:
            appointment_id = booking.__getattribute__("id")
            booked_start_time = booking.__getattribute__("start")
            student_name = booking.__getattribute__("full_name")
            studio_name = booking.__getattribute__("res_name")
            the_date = datetime.datetime.fromisoformat(booked_start_time).date()
            if the_date != datetime.datetime.today().date():
                log = f"{student_name}'s {studio_name} booking for " \
                      f"{datetime.datetime.fromisoformat(booked_start_time).strftime('%m/%d %I:%M%p')} has been deleted."
                self._app.print_output(log)
                # self._google_sheets.log_to_log_book(student_object, log)
                self._client.appointments.delete(self._schedule_id, appointment_id)

    def block_student(self, student_id, supersaas_id, booking):
        the_date = datetime.datetime.today().date().isoformat()
        # student_name = self._student_holder.get_student_by_student_id(student_id).get_full_name()
        the_student_object = self._student_holder.get_student_by_student_id(student_id)

        self._database.add_student_to_block_list(student_id, the_student_object.get_proper_name(), the_date)

        # Log the info
        log = f"Blocked {the_student_object.get_full_name()} for missed {booking.__getattribute__('res_name')} booking."
        self._app.print_output(log)
        # self._google_sheets.log_to_log_book(the_student_object, log)

        # Update credits to 0
        new_attributes = {"credit": "0"}
        self._client.users.update(supersaas_id, new_attributes)

        # Get Agenda and cancel those bookings
        future_bookings = self.get_list_of_bookings_from_agenda(supersaas_id)
        self.remove_bookings_from_list(future_bookings)

        # Send Email to student
        the_emailer_gmail.send_missed_booking_email(the_student_object, booking)

    def get_number_of_current_users(self):
        self.setup_student_holder()
        return len(self._all_users)

    def get_number_of_current_bookings(self):
        self.set_all_bookings()
        return len(self._all_bookings)


if __name__ == "__main__":
    db = DatabaseInfo()
    student_object = db.get_student_object_from_id(21080483)
    print(student_object)
