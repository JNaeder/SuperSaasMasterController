from SuperSaaS import Client, Configuration
import gspread
import datetime


class StudentClass:
    def __init__(self, student_id="", full_name="", icr=0.0, gpa=0.0, mod="", saas_id=""):
        self._student_id = student_id
        self._full_name = full_name
        self._icr = icr
        self._gpa = gpa
        self._mod = mod
        self._saas_id = saas_id

    def __repr__(self):
        output = f"{self._full_name} ({self._student_id}) GPA: {self._gpa} ICR: {self._icr} {self._mod} saas_id: {self._saas_id}"
        return output

    def get_student_id(self):
        return self._student_id

    def get_full_name(self):
        return self._full_name

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


class StudentObjectHolder:
    def __init__(self):
        self._list_of_student_objects = []

    def get_list_of_student_objects(self):
        return self._list_of_student_objects

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

    def get_student_by_saas_id(self, saas_id):
        for student in self._list_of_student_objects:
            if student.get_saas_id() == saas_id and saas_id != "":
                return student
        return None


class GoogleSheets:
    def __init__(self, student_holder):
        google_sheet = gspread.oauth()
        main_spreadsheet = google_sheet.open_by_key('1yiElZvxpOt_iH9aDxsm_fOPs5BTTkff_ijZjwqgIsmU')
        other_stuff_spreadsheet = google_sheet.open_by_key('17IIW21BzwSirT5g53Un9oYEZUSB0CaRmS55f9ur8n94')
        grads_sheet = other_stuff_spreadsheet.worksheet("Grads")
        preferred_name_sheet = other_stuff_spreadsheet.worksheet("Preferred Names")
        all_active_worksheet = main_spreadsheet.worksheet("All Active")
        icr_gpa_worksheet = main_spreadsheet.worksheet("Running GPA and ICR")
        self._students_ids = icr_gpa_worksheet.col_values(1)
        self._student_full_names = icr_gpa_worksheet.col_values(2)
        self._icrs = icr_gpa_worksheet.col_values(3)
        self._gpas = icr_gpa_worksheet.col_values(4)
        self._all_active_names = all_active_worksheet.col_values(1)
        self._all_active_student_id = all_active_worksheet.col_values(2)
        self._all_active_mod = all_active_worksheet.col_values(3)
        self._grads_student_ids = grads_sheet.col_values(2)
        self._grad_full_names = grads_sheet.col_values(1)
        self._preferred_name_real = preferred_name_sheet.col_values(1)
        self._preferred_name_preferred = preferred_name_sheet.col_values(2)
        self._student_holder = student_holder

        for the_id in self._students_ids:
            new_student = self.get_student_object_from_id(the_id)
            self._student_holder.add_student(new_student)
        for the_id in self._grads_student_ids:
            new_student = self.get_student_object_from_id(the_id)
            self._student_holder.add_student(new_student)

    def get_student_ids(self):
        return self._students_ids

    def get_student_icrs(self):
        return self._icrs

    def get_student_gpas(self):
        return self._gpas

    def get_student_object_from_id(self, student_id):
        full_name = ""
        icr = 0.0
        gpa = 0.0
        mod = ""
        if student_id in self._students_ids:
            for index in range(1, len(self._students_ids)):
                if self._students_ids[index] == student_id:
                    icr = float(self._icrs[index][0:-1])
                    gpa = float(self._gpas[index])
                    full_name = self._student_full_names[index]
            for index in range(len(self._all_active_student_id)):
                if self._all_active_student_id[index] == student_id:
                    mod = "Mod " + self._all_active_mod[index][4]
            for index in range(len(self._preferred_name_real)):
                if self._preferred_name_real[index] == full_name:
                    print(f"Changed {self._preferred_name_real[index]} to {self._preferred_name_preferred[index]}")
                    full_name = self._preferred_name_preferred[index]
            new_student = StudentClass(student_id, full_name, icr, gpa, mod)
            return new_student
        elif student_id in self._grads_student_ids:
            for index in range(1, len(self._grads_student_ids)):
                if self._grads_student_ids[index] == student_id:
                    full_name = self._grad_full_names[index]
                    mod = "Graduate"
            for index in range(len(self._preferred_name_real)):
                if self._preferred_name_real[index] == full_name:
                    full_name = self._preferred_name_preferred[index]
            new_student = StudentClass(student_id, full_name, 100, 4, mod)
            return new_student

        return None


class SuperSaasController:
    def __init__(self, student_holder, icr_cutoff):
        config = Configuration()
        self._client = Client(config)
        self._client.account_name = "SAE_New_York"
        self._client.api_key = "DB15OLn37rWxCBMrTBCiWw"
        self._schedule_id = "510374"
        date_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        self._all_bookings = self._client.appointments.list(schedule_id=self._schedule_id, limit=100,
                                                            start_time=date_today)
        self._all_users = self._client.users.list(form=False, limit=500)
        self._icr_cutoff = icr_cutoff
        self._student_holder = student_holder
        self.update_student_holder()

    def update_student_holder(self):
        for user in self._all_users:
            student_id = user.__getattribute__("name").split(".")[0]
            supersaas_id = user.__getattribute__("id")
            self._student_holder.add_parameter_by_id(student_id, supersaas_id)

    def go_through_all_users(self):
        for user in self._all_users:
            ss_full_name = user.__getattribute__("full_name")
            supersaas_id_num = user.__getattribute__("id")
            ss_credits = user.__getattribute__('credit')
            student_object = self._student_holder.get_student_by_saas_id(supersaas_id_num)
            # print(student_object)
            if student_object is not None:
                if student_object.get_full_name() != ss_full_name:
                    new_attributes = {
                        "full_name": student_object.get_full_name()
                    }
                    self.update_user(supersaas_id_num, new_attributes)

                if student_object.get_icr() < self._icr_cutoff:
                    if ss_credits != "0":
                        print(f"{student_object.get_full_name()} is now below ICR CUTOFF")
                        new_attributes = {
                            "credit": "0"
                        }
                        self.update_user(supersaas_id_num, new_attributes)
                elif ss_credits != "-":
                    print(f"{student_object.get_full_name()} is now above ICR CUTOFF")
                    new_attributes = {
                        "credit": "-"
                    }
                    self.update_user(supersaas_id_num, new_attributes)
            else:
                print(f"{ss_full_name} is not an active student")

    def update_user(self, supersaas_id, attributes):
        self._client.users.update(supersaas_id, attributes)
        if "full_name" in attributes:
            print(f"Updated {attributes['full_name']}'s name in SuperSaas")
        if "credit" in attributes:
            print(f"Updated credits")

    def go_through_all_bookings(self):
        for booking in self._all_bookings:
            student_name = booking.__getattribute__("full_name")
            mod = booking.__getattribute__("field_1_r")
            booking_id = booking.__getattribute__("id")
            student_supersaas_id = booking.__getattribute__("user_id")
            student_object = self._student_holder.get_student_by_saas_id(student_supersaas_id)
            if student_object is not None:
                if student_object.get_full_name() != student_name:
                    attributes = {
                        "full_name": student_object.get_full_name(),
                        "name": student_object.get_student_id() + ".us@saeinstitute.edu"
                    }
                    self._client.appointments.update(self._schedule_id, booking_id, attributes)
                    print(f"Changed {student_object.get_full_name()}'s name to real name.")
                if student_object.get_mod() != mod:
                    attributes = {
                        "field_1_r": student_object.get_mod(),
                        "name": student_object.get_student_id() + ".us@saeinstitute.edu"
                    }
                    self._client.appointments.update(self._schedule_id, booking_id, attributes)
                    print(f"Changed {student_object.get_full_name()}'s mod to the correct mod")


sh = StudentObjectHolder()
gs = GoogleSheets(sh)
ss = SuperSaasController(sh, 80)
ss.go_through_all_users()
ss.go_through_all_bookings()
