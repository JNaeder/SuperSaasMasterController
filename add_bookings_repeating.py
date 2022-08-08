from SuperSaaS import Client, Configuration
from dateutil.parser import *
import dateutil

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


def create_booking(teacher_info_list, the_studio, the_date, start_time, end_time):
    full_name = teacher_info_list[0]
    booking_id = teacher_info_list[1]
    email = teacher_info_list[2]
    studio_id = get_resource_id_by_name(the_studio)
    attributes = {
        "name": email,
        'resource_id': studio_id,
        "full_name": full_name,

    }
    client.appointments.create(schedule_id=schedule_id, user_id=booking_id, attributes=attributes)


sample_date = "8/8/22"
sample_start_time = "2:00pm"
sample_end_time = "4:00pm"

start_date = f"{sample_date} {sample_start_time}"
end_date = f"{sample_date} {sample_end_time}"
print(start_date)
print(end_date)
str_obj = parser.parse(start_date)
print(str_obj)

# def create_booking(booking_id, email)
#
# print(get_booking_id_by_name("Dan Grigsby"))
