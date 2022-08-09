import datetime


class TeacherBooking:
    def __init__(self, sscontrol):
        self._sscontrol = sscontrol
        self._resource_dict = {
            "SSL": 772666,
            "Audient": 740583,
            "Production Suite 1": 740582,
            "Production Suite 2": 772665,
            "Production Suite 3": 866791,
            "Production Suite 4": 866792,
            "02R": 740584,
            "Avid S6": 740587
        }
        self._days_of_class = ["Monday", "Tuesday", "Wednesday", "Thursday"]

    def get_list_of_dates_for_term(self, start_date, end_date):
        output = []
        while start_date <= end_date:
            day_of_the_week = start_date.strftime("%A")
            if day_of_the_week in self._days_of_class:
                output.append(start_date)
            start_date += datetime.timedelta(days=1)
        return output

    def get_teacher_info_by_name(self, the_name):
        for user in self._sscontrol.get_all_users():
            full_name = user.__getattribute__("full_name")
            booking_id = user.__getattribute__("id")
            if the_name == full_name:
                output_list = [full_name, booking_id]
                return output_list
        return None

    def get_resource_id_by_name(self, the_name):
        if the_name in self._resource_dict:
            return self._resource_dict[the_name]
        return None

    def create_booking(self, teacher_info_list, studio_id, the_mod, start_datetime, end_datetime):
        full_name = teacher_info_list[0]
        booking_id = teacher_info_list[1]
        attributes = {
            'resource_id': studio_id,
            "full_name": full_name,
            "start": start_datetime.isoformat(),
            "finish": end_datetime.isoformat(),
            "field_1_r": f"Mod {the_mod}"
        }
        self._sscontrol.create_booking(booking_id, attributes)

    def create_repeating_bookings(self, the_name, the_studio, the_mod, start_time, length, list_of_dates):
        teacher_info = self.get_teacher_info_by_name(the_name)
        studio_id = self.get_resource_id_by_name(the_studio)
        for the_date in list_of_dates:
            the_time = datetime.time(start_time, 0, 0)
            start_datetime = datetime.datetime.combine(the_date, the_time)
            end_time = start_datetime + datetime.timedelta(0, 0, 0, 0, 0, length, 0)
            self.create_booking(teacher_info, studio_id, the_mod, start_datetime, end_time)
