import SuperSaaS.Error
from SuperSaaS import Client, Configuration
import gspread
import datetime
import json
from add_bookings_repeating import TeacherBooking


class StudentClass:
    def __init__(self, student_id, proper_name, icr, gpa, mod, saas_id="", the_credits=""):
        self._student_id = student_id
        self._proper_name = proper_name
        self._icr = icr
        self._gpa = gpa
        self._mod = mod
        self._saas_id = saas_id
        self._credits = the_credits
        self._last_name = self._proper_name.split(', ')[0]
        self._first_name = self._proper_name.split(', ')[1]
        self._full_name = f"{self._first_name} {self._last_name}"

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

    def add_student(self, student_object):
        self._list_of_student_objects.append(student_object)

    def add_parameter_by_id(self, student_id, parameter):
        student = self.get_student_by_student_id(student_id)
        if student is not None:
            student.set_saas_id(parameter)

    def get_student_by_student_id(self, student_id):
        for student in self._list_of_student_objects:
            if student.get_student_id() == student_id:
                return student
        return None


class GoogleSheets:
    def __init__(self):
        # Worksheets
        self._log_book = None
        # ICR/GPA of Values
        self._students_ids = None
        self._icrs = None
        self._gpas = None
        # All Active Values
        self._all_active_proper_name = None
        self._all_active_student_id = None
        self._all_active_mod = None
        # Grads Values
        self._grads_student_ids = None
        self._grad_full_names = None
        # Preferred Name Values
        self._preferred_name_real = None
        self._preferred_name_preferred = None

    def info_is_there(self):
        if self._students_ids is None:
            return False
        return True

    def get_spreadsheet_info(self):
        # OAuth
        google_sheet = gspread.oauth()
        # Spreadsheets
        main_spreadsheet = google_sheet.open_by_key('1yiElZvxpOt_iH9aDxsm_fOPs5BTTkff_ijZjwqgIsmU')
        other_stuff_spreadsheet = google_sheet.open_by_key('17IIW21BzwSirT5g53Un9oYEZUSB0CaRmS55f9ur8n94')
        # Worksheets
        grads_sheet = other_stuff_spreadsheet.worksheet("Grads")
        preferred_name_sheet = other_stuff_spreadsheet.worksheet("Preferred Names")
        self._log_book = other_stuff_spreadsheet.worksheet("Log Book")
        all_active_worksheet = main_spreadsheet.worksheet("All Active")
        icr_gpa_worksheet = main_spreadsheet.worksheet("Running GPA and ICR")
        # ICR/GPA of Values
        self._students_ids = icr_gpa_worksheet.col_values(1)
        self._icrs = icr_gpa_worksheet.col_values(3)
        self._gpas = icr_gpa_worksheet.col_values(4)
        # All Active Values
        self._all_active_proper_name = all_active_worksheet.col_values(1)
        self._all_active_student_id = all_active_worksheet.col_values(2)
        self._all_active_mod = all_active_worksheet.col_values(3)
        # Grads Values
        self._grads_student_ids = grads_sheet.col_values(2)
        self._grad_full_names = grads_sheet.col_values(1)
        # Preferred Name Values
        self._preferred_name_real = preferred_name_sheet.col_values(1)
        self._preferred_name_preferred = preferred_name_sheet.col_values(2)

    def get_student_object_from_id(self, student_id, the_name="", email_end=""):
        proper_name = ""
        icr = 0.0
        gpa = 0.0
        mod = ""
        # Check that ID from SuperSaas is in both academic sheets
        if student_id in self._students_ids and student_id in self._all_active_student_id:
            # Loop through all the IDs in the ICR Sheet
            for index in range(1, len(self._students_ids)):
                if self._students_ids[index] == student_id:
                    icr = float(self._icrs[index][0:-1])
                    gpa = float(self._gpas[index])
            # Loop through all the IDs in the Active Sheet
            for index in range(len(self._all_active_student_id)):
                if self._all_active_student_id[index] == student_id:
                    if self._all_active_mod[index] == "#N/A":
                        mod = "Graduate"
                        icr = "-"
                        gpa = "-"
                    else:
                        mod = "Mod " + self._all_active_mod[index][4]
                        proper_name = self._all_active_proper_name[index]
            # Checking for preferred names
            for index in range(len(self._preferred_name_real)):
                if self._preferred_name_real[index] == proper_name:
                    proper_name = self._preferred_name_preferred[index]
            # Create new Student object
            new_student = StudentClass(student_id, proper_name, icr, gpa, mod)
            return new_student
        # Check if student ID is in the Grad sheet
        elif student_id in self._grads_student_ids:
            for index in range(1, len(self._grads_student_ids)):
                if self._grads_student_ids[index] == student_id:
                    proper_name = self._grad_full_names[index]
                    mod = "Graduate"
            for index in range(len(self._preferred_name_real)):
                if self._preferred_name_real[index] == proper_name:
                    proper_name = self._preferred_name_preferred[index]
            new_student = StudentClass(student_id, proper_name, "-", "-", mod)
            return new_student
        # Check if they have a student email. Make empty student object with it.
        elif email_end != "sae.edu":
            name_split = the_name.split(" ")
            if len(name_split) > 2:
                proper_name = f"{the_name.split(' ')[1]}, {the_name.split(' ')[0]}"
            else:
                proper_name = the_name
            new_student = StudentClass(student_id, proper_name, 0, 0, "NOT ACTIVE")
            return new_student
        return None

    def log_to_log_book(self, student_object, the_log):
        student_name = student_object.get_full_name()
        student_id = student_object.get_student_id()
        the_datetime = datetime.datetime.now()
        the_date = the_datetime.strftime("%m/%d/%Y")
        the_time = the_datetime.strftime("%H:%M:%S")
        log_list = [student_name, student_id, the_date, the_time, the_log]
        self._log_book.append_row(log_list)


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
        self._google_sheets = GoogleSheets()
        self._teacher_booking = TeacherBooking(self)
        self._number_of_changes = 0

        self.read_json_data()

    def set_app(self, app):
        self._app = app

    def read_json_data(self):
        with open("data.json", "r") as the_file:
            the_data = json.load(the_file)
        self._icr_cutoff = the_data["icr"]
        self._gpa_cutoff = the_data["gpa"]
        self._client.account_name = the_data["account_name"]
        self._client.api_key = the_data["api_key"]
        self._schedule_id = the_data["schedule_id"]

    def info_is_there(self):
        if self._google_sheets.info_is_there() and self._all_users is not None:
            return True
        return False

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
        self.read_json_data()
        self._google_sheets.get_spreadsheet_info()
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
            new_student = self._google_sheets.get_student_object_from_id(student_id, the_name, email_end)
            if new_student is not None:
                new_student.set_saas_id(supersaas_id)
                new_student.set_credits(ss_credit)
                self._student_holder.add_student(new_student)

    def set_all_bookings(self):
        date_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        self._all_bookings = self._client.appointments.list(schedule_id=self._schedule_id, limit=500,
                                                            start_time=date_today)

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
        student_object = self._google_sheets.get_student_object_from_id(student_id)
        name = student_object.get_full_name()
        if student_object.get_mod() == "Graduate":
            return True
        student_mod = int(student_object.get_mod()[-1])
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
            student_object = self._student_holder.get_student_by_student_id(student_id)
            if student_object is not None:
                correct_full_name = student_object.get_full_name()
                student_icr = student_object.get_icr()
                student_gpa = student_object.get_gpa()
                # If the student is listed as a graduate
                if student_object.get_mod() == "Graduate" and ss_credits != "-":
                    log = f"{correct_full_name} is a graduate. Credits set to infinity"
                    self.increase_number_of_changes()
                    self._app.print_output(log)
                    self._google_sheets.log_to_log_book(student_object, log)
                    new_attributes = {
                        "credit": "-"
                    }
                    self._client.users.update(supersaas_id_num, new_attributes)
                    student_object.set_credits("-")
                if student_object.get_mod() != "Graduate":
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
                        self._google_sheets.log_to_log_book(student_object, log)

                    # Check if user's credits need to change based on if they can book or not.
                    if ss_credits != "-":
                        if can_book:
                            log = f"{correct_full_name} is now able to book. Credits updated to infinity"
                            self.increase_number_of_changes()
                            self._app.print_output(log)
                            self._google_sheets.log_to_log_book(student_object, log)
                            new_attributes = {
                                "credit": "-"
                            }
                            self._client.users.update(supersaas_id_num, new_attributes)
                            student_object.set_credits("-")
                    elif ss_credits != "0":
                        if not can_book:
                            if student_icr < self._icr_cutoff:
                                log = f"{correct_full_name} is now below the {self._icr_cutoff}% " \
                                      f"ICR cutoff. Credits have been set to 0"
                            else:
                                log = f"{correct_full_name} is now below the {self._gpa_cutoff} " \
                                      f"GPA cutoff. Credits have been set to 0"
                            self.increase_number_of_changes()
                            self._app.print_output(log)
                            self._google_sheets.log_to_log_book(student_object, log)
                            new_attributes = {
                                "credit": "0"
                            }
                            self._client.users.update(supersaas_id_num, new_attributes)
                            student_object.set_credits("0")

            # Check if user is not in the academic system, or not an employee
            elif email_ending != "sae.edu" and ss_credits != "0":
                new_attributes = {
                    "credit": "0"
                }
                self._client.users.update(supersaas_id_num, new_attributes)
                student_object.set_credits("0")
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
            student_object = self._student_holder.get_student_by_student_id(student_id)
            # If student object exists
            if student_object is not None:
                correct_mod = student_object.get_mod()
                correct_name = student_object.get_full_name()
                correct_student_id = student_object.get_student_id()

                # Checks to see if student is allowed to make the booking.
                if not self.booking_is_valid(student_id, booked_room):
                    booking_time = datetime.datetime.fromisoformat(booking_start_time)
                    log = f"***BOOKING NOT ALLOWED***: {correct_name} in {correct_mod} booked the {booked_room} " \
                          f"on {booking_time.strftime('%A %m/%d at %H:%M')}"
                    self._app.print_output(log)

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
                    self._google_sheets.log_to_log_book(student_object, log)

                # Runs when the mod of the booking doesn't match the mod in the system
                if correct_mod != mod:
                    attributes = {
                        "field_1_r": correct_mod,
                        "name": correct_student_id + ".us@saeinstitute.edu"
                    }
                    try:
                        self._client.appointments.update(self._schedule_id, booking_id, attributes)
                        booking_time = datetime.datetime.fromisoformat(booking_start_time)
                        log = f"{correct_name}'s Mod has been updated for {booked_room} booking for " \
                              f"{booking_time.strftime('%A %m/%d')}"
                        self.increase_number_of_changes()
                        self._app.print_output(log)
                        self._google_sheets.log_to_log_book(student_object, log)
                    except SuperSaaS.Error as error:
                        log = f"There was an error updating {correct_name}'s booking."
                        self._app.print_output(error)
                        self._app.print_output(log)

    def get_number_of_current_users(self):
        self.setup_student_holder()
        return len(self._all_users)

    def get_number_of_current_bookings(self):
        self.set_all_bookings()
        return len(self._all_bookings)


if __name__ == "__main__":
    ss = SuperSaasController()
    ss.get_all_info()
    tb = ss.get_teacher_booking()
    # august_dates = tb.get_list_of_dates_for_term(datetime.datetime(2022, 8, 8), datetime.datetime(2022, 8, 18))
    # tb.create_repeating_bookings("Abe Silver", "Audient", 2, 14, 4, august_dates)
