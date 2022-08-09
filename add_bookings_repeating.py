import datetime

from SuperSaaS import Client, Configuration

config = Configuration()
client = Client(config)
client.account_name = "SAE_New_York"
client.api_key = "DB15OLn37rWxCBMrTBCiWw"
schedule_id = "510374"
resource_dict = {
    "SSL": 772666,
    "Audient": 740583,
    "Production Suite 1": 740582,
    "Production Suite 2": 772665,
    "Production Suite 3": 866791,
    "Production Suite 4": 866792,
    "02R": 740584,
    "Avid S6": 740587
}

all_users = client.users.list(form=False, limit=500)

# all_bookings = client.appointments.list(schedule_id=schedule_id, limit=500)
# print(all_bookings)


term_start_date = datetime.date(2022, 8, 8)
term_end_date = datetime.date(2022, 10, 27)


def get_list_of_dates_for_term(start_date, end_date):
    for month in range(start_date.month, end_date.month + 1):
        print(month)


get_list_of_dates_for_term(term_start_date, term_end_date)


def get_booking_info_by_name(the_name):
    for user in all_users:
        full_name = user.__getattribute__("full_name")
        booking_id = user.__getattribute__("id")
        email = user.__getattribute__("name")
        if the_name == full_name:
            output_list = [full_name, booking_id, email]
            return output_list
    return None


def get_resource_id_by_name(the_name):
    if the_name in resource_dict:
        return resource_dict[the_name]
    return None


def create_booking(teacher_info_list, studio_id, the_mod, start_datetime, end_datetime):
    full_name = teacher_info_list[0]
    booking_id = teacher_info_list[1]
    email = teacher_info_list[2]
    attributes = {
        "name": email,
        'resource_id': studio_id,
        "full_name": full_name,
        "start": start_datetime.isoformat(),
        "finish": end_datetime.isoformat(),
        "field_1_r": f"Mod {the_mod}"
    }
    client.appointments.create(schedule_id=schedule_id, user_id=booking_id, attributes=attributes)


def create_repeating_bookings(the_name, the_studio, the_mod, start_time, length, list_of_dates):
    booking_id = get_booking_info_by_name(the_name)
    studio_id = get_resource_id_by_name(the_studio)
    for the_date in list_of_dates:
        the_time = datetime.time(start_time, 0, 0)
        start_datetime = datetime.datetime.combine(the_date, the_time)
        end_time = start_datetime + datetime.timedelta(0, 0, 0, 0, 0, length, 0)
        create_booking(booking_id, studio_id, the_mod, start_datetime, end_time)


# create_repeating_bookings("Dan Grigsby", "SSL", 3, 14, 4)
# create_repeating_bookings("Abe Silver", "Audient", 2, 14, 4)
