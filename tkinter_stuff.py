import time
import datetime
import threading
import tkinter as tk
from tkinter import ttk
from SuperSaasController import SuperSaasController
import webbrowser
from PIL import Image, ImageTk
from SettingsScreen import SettingsScreen
from Image_Bundler import create_path


class App(tk.Tk):
    def __init__(self, sscontrol: SuperSaasController):
        super().__init__()
        self.config(background="#292929")
        self.state("zoomed")
        # Value Variables
        self.output_value = tk.StringVar()
        # Outside Objects
        self.supersaas_controller = sscontrol

        # Setup
        self.title("SAE NYC Booking Manager")
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}")
        # self.attributes("-fullscreen", True)
        self.style = StyleClass(self)

        # Frames
        self.title_frame = TitleFrame(self)
        self.left_side_frame = LeftSideFrame(self)
        self.right_side_frame = RightSideFrame(self)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
        self.left_side_frame.grid(row=1, column=0, sticky="nsew")
        self.right_side_frame.grid(row=1, column=1, sticky="nsew")

        self.print_output("Welcome to SAE NYC Booking Manager.")

        new_thread = threading.Thread(target=self.check_everything, daemon=True)
        new_thread.start()

    def print_output(self, output_text):
        self.left_side_frame.output_screen.print_output(output_text)

    def check_everything(self):
        while True:
            self.supersaas_controller.get_all_info()
            self.supersaas_controller.go_through_all_users()
            self.supersaas_controller.go_through_all_bookings()
            time.sleep(30)


class StyleClass(ttk.Style):
    def __init__(self, container: App):
        super().__init__(container)

        background_white = "#FFFFFF"
        background_dark = "#292929"
        # sae_blue = "#307FE2"
        sae_teal = "#00B0B9"
        sae_red = "#EE2737"
        # sae_yellow = "#FFB500"
        # sae_light_blue = "#58c9e6"

        self.theme_use("default")

        self.configure("TFrame", background=background_dark)

        self.configure("TLabel", background=background_dark, foreground="white")
        self.configure("OPEN.TLabel", background=background_dark, foreground="white")
        self.configure("CLOSED.TLabel", background=sae_teal, foreground="white")
        self.configure("BLOCKED.TLabel", background=sae_red, foreground="white")

        self.configure("TButton", background=background_white, foreground=background_dark,
                       relief="solid", borderwidth=2, padding=0)
        self.configure("Title.TButton", background=background_dark, relief="flat")
        self.configure("Big.TButton", background=background_white, font=("Arial", 15),
                       foreground=background_dark, relief="solid", borderwidth=2)


# noinspection PyGlobalUndefined,PyTypeChecker
class TitleFrame(ttk.Frame):
    def __init__(self, container: App):
        super().__init__(container)
        global logo, settings_icon_image, web_icon_image, refresh_icon_image, teacher_icon_image

        self.controller = container
        # Variables
        logo = ImageTk.PhotoImage(Image.open(create_path('imgs/Transparent Smaller.png')).resize(size=(128, 128)))
        refresh_icon_image = ImageTk.PhotoImage(Image.open(create_path('imgs/refresh.png')).resize(size=(64, 64)))
        settings_icon_image = ImageTk.PhotoImage(Image.open(create_path('imgs/settings.png')).resize(size=(64, 64)))
        web_icon_image = ImageTk.PhotoImage(Image.open(create_path('imgs/internet.png')).resize(size=(64, 64)))
        teacher_icon_image = ImageTk.PhotoImage(Image.open(create_path('imgs/teacher.png')).resize(size=(64, 64)))

        # Widgets
        logo_label = ttk.Label(self, image=logo, padding=(50, 0, 50, 0))
        title_label = ttk.Label(self, text="SAE NYC Booking Manager", foreground="White", font=("Arial", 35))

        button_frame = ttk.Frame(self)

        settings_icon = ttk.Button(button_frame, image=settings_icon_image,
                                   command=self.open_settings_page, style="Title.TButton")
        web_icon = ttk.Button(button_frame, image=web_icon_image,
                              command=self.open_web_pages, style="Title.TButton")
        teacher_icon = ttk.Button(button_frame, image=teacher_icon_image,
                                  command=self.open_teacher_booking_page, style="Title.TButton")

        seperator = ttk.Separator(self, orient="horizontal")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Layout
        logo_label.grid(row=0, column=0, sticky="e")
        title_label.grid(row=0, column=1, sticky="w")

        button_frame.grid(row=0, column=3, sticky="ew")

        settings_icon.grid(row=0, column=1, padx=5)
        web_icon.grid(row=0, column=2, padx=5)
        teacher_icon.grid(row=0, column=3, padx=5)

        seperator.grid(row=1, column=0, columnspan=5, sticky="ew")

    def open_settings_page(self):
        settings_page = SettingsScreen(self.controller)
        settings_page.mainloop()

    def open_web_pages(self):
        webbrowser.open(
            "https://docs.google.com/spreadsheets/d/17IIW21BzwSirT5g53Un9oYEZUSB0CaRmS55f9ur8n94/edit#gid=1026026296")
        webbrowser.open("https://supersaas.com/schedule/SAE_New_York/5th_Floor_Booking")
        self.controller.print_output("Web pages open")

    def open_teacher_booking_page(self):
        teacher_booking_page = TeacherBookingScreen(self.controller)
        teacher_booking_page.mainloop()


class RightSideFrame(ttk.Frame):
    def __init__(self, container: App):
        super().__init__(container, padding=(20, 0))
        self.controller = container
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=0, sticky="ew")

        student_list_button = ttk.Button(self, text="Student List",
                                         command=self.open_student_list_page, style="Big.TButton")
        today_bookings_button = ttk.Button(self, text="Today's Bookings",
                                           command=self.get_today_bookings, style="Big.TButton")

        today_bookings_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=20, ipady=2)
        student_list_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=20, ipady=2)

        self.student_list_page = None
        self.today_booking_screen = None

        self.get_today_bookings()

    def open_student_list_page(self):
        if self.student_list_page is not None:
            self.student_list_page.destroy()
        self.student_list_page = StudentListScreen(self)
        self.student_list_page.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.student_list_page.columnconfigure(0, weight=1)
        self.student_list_page.rowconfigure(0, weight=1)

    def get_today_bookings(self):
        if self.today_booking_screen is not None:
            self.today_booking_screen.destroy()
        bookings = self.controller.supersaas_controller.get_bookings_for_today()
        self.today_booking_screen = TodayBookingScreen(self, bookings)
        self.today_booking_screen.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.today_booking_screen.columnconfigure(0, weight=1)
        self.today_booking_screen.rowconfigure(0, weight=1)


class LeftSideFrame(ttk.Frame):
    def __init__(self, container: App):
        super().__init__(container, padding=(20, 10))
        self.controller = container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.output_screen = OutputScreen(self)
        self.output_screen.grid(row=1, column=0, sticky="nsew")


class OutputScreen(ttk.Frame):
    def __init__(self, container: LeftSideFrame):
        super().__init__(container)
        self.screen = tk.Text(self, state="disabled", background="black", foreground="white",
                              font=("Arial", 15), wrap="word")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.screen.grid(sticky="nsew", pady=20)

    def print_output(self, output_text):
        self.screen.config(state="normal")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        final_output = f"{current_time}: {output_text}\n"
        self.screen.insert("1.0", final_output)
        self.screen.config(state="disabled")


# noinspection PyTypeChecker
class TeacherBookingScreen(tk.Toplevel):
    def __init__(self, container):
        super().__init__(container)
        self.controller = container
        self.configure(background="#292929")

        # Text Variables
        self.name_selection_var = tk.StringVar()
        self.mod_selection_var = tk.StringVar()
        self.studio_selection_var = tk.StringVar()
        self.time_start_var = tk.StringVar()
        self.time_end_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        # Setup
        self.title("Teacher Booking")
        self.config(padx=50, pady=50)
        self.resizable(False, False)

        # Widgets
        name_selection_label = ttk.Label(self, text="Name: ")
        name_selection = ttk.Combobox(self, textvariable=self.name_selection_var, state="readonly")
        name_selection['value'] = self.controller.supersaas_controller.get_employee_list()
        mod_selection_label = ttk.Label(self, text="Mod: ")
        mod_selection = ttk.Combobox(self, textvariable=self.mod_selection_var, state="readonly")
        mod_selection['values'] = ("Mod 1", "Mod 2", "Mod 3", "Mod 4")
        studio_selection_label = ttk.Label(self, text="Studio: ")
        studio_selection = ttk.Combobox(self, textvariable=self.studio_selection_var, state="readonly")
        # studio_selection['values'] = ("SSL", "Audient", "Avid S6", "02R", "Production Suite 1", "Production Suite 2",
        #                               "Production Suite 3", "Production Suite 4")
        studio_selection['values'] = \
            list(self.controller.supersaas_controller.get_teacher_booking().get_resource_dict().keys())
        time_start_label = ttk.Label(self, text="Start Time: ")
        time_start_entry = ttk.Entry(self, textvariable=self.time_start_var)
        time_end_label = ttk.Label(self, text="End Time: ")
        time_end_entry = ttk.Entry(self, textvariable=self.time_end_var)
        start_date_label = ttk.Label(self, text="Start Date: ")
        start_date_entry = ttk.Entry(self, textvariable=self.start_date_var)
        end_date_label = ttk.Label(self, text="End Date: ")
        end_date_entry = ttk.Entry(self, textvariable=self.end_date_var)
        submit_button = ttk.Button(self, text="Book", command=self.submit_button)

        # Layout
        name_selection_label.grid(row=0, column=0)
        name_selection.grid(row=0, column=1)
        mod_selection_label.grid(row=1, column=0)
        mod_selection.grid(row=1, column=1)
        studio_selection_label.grid(row=2, column=0)
        studio_selection.grid(row=2, column=1)
        time_start_label.grid(row=3, column=0)
        time_start_entry.grid(row=3, column=1)
        time_end_label.grid(row=4, column=0)
        time_end_entry.grid(row=4, column=1)
        start_date_label.grid(row=5, column=0)
        start_date_entry.grid(row=5, column=1)
        end_date_label.grid(row=6, column=0)
        end_date_entry.grid(row=6, column=1)
        submit_button.grid(row=30, column=0, columnspan=2)

        for child in self.winfo_children():
            child.grid_configure(pady=2, sticky="we")
            if "label" in child.winfo_name():
                child.grid_configure(sticky="e")

    def submit_button(self):
        the_name = self.name_selection_var.get()
        the_mod = int(self.mod_selection_var.get()[4])
        the_studio = self.studio_selection_var.get()
        start_time = float(self.time_start_var.get())
        end_time = int(self.time_end_var.get())
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        self.controller.supersaas_controller.set_repeating_bookings(the_name, the_mod, the_studio, start_time,
                                                                    end_time, start_date, end_date)
        self.controller.print_output(f"Booked {the_studio} for {the_name}, from {start_date} to {end_date}")
        self.destroy()


# noinspection PyTypeChecker
class StudentListScreen(ttk.Frame):
    def __init__(self, container: RightSideFrame):
        super().__init__(container)
        self.background_color = None
        self.controller = container
        self.configure(padding=(10, 10))

        self.the_frame = tk.Frame(self, height=self.controller.controller.height)
        self.the_frame.columnconfigure(0, weight=1)
        self.the_frame.rowconfigure(0, weight=1)

        self.the_canvas = tk.Canvas(self.the_frame, height=self.controller.controller.height, bg="#292929", bd=0)
        self.scroll_bar = ttk.Scrollbar(self, orient="vertical", command=self.the_canvas.yview)

        self.scrollable_frame = ttk.Frame(self.the_canvas, padding=0)
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.the_canvas.configure(scrollregion=self.the_canvas.bbox("all")))
        # self.scrollable_frame.columnconfigure(0, weight=1)

        self.the_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.the_canvas.config(yscrollcommand=self.scroll_bar.set, background="#292929")

        self.the_frame.grid(sticky="nsew")
        self.the_canvas.grid(sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")

        self.show_list()

    @staticmethod
    def get_key(some_object):
        return some_object.get_last_name()

    def show_list(self):
        list_of_students = self.controller.controller.supersaas_controller.get_student_holder() \
            .get_list_of_student_objects()
        list_of_students.sort(key=self.get_key)
        for index in range(len(list_of_students)):
            student_object = list_of_students[index]
            formal_name = student_object.get_proper_name()
            mod = student_object.get_mod()
            icr = student_object.get_icr()
            gpa = student_object.get_gpa()
            the_credits = student_object.get_credits()
            self.background_color = "#3f7343"

            if mod == "NOT ACTIVE":
                # self.background_color = self.controller.background_color
                pass
            elif the_credits == "0":
                self.background_color = "#aa0808"
            elif mod == "Graduate":
                self.background_color = "#3f5473"

            info_frame = tk.LabelFrame(self.scrollable_frame, background=self.background_color)
            info_frame.grid(sticky="ew", pady=5)

            name_label = ttk.Label(info_frame, text=formal_name, font=("Arial", 15), background=self.background_color)
            mod_label = ttk.Label(info_frame, text=mod, font=("Arial", 10), background=self.background_color)
            icr_label = ttk.Label(info_frame, text=f"ICR: {icr}%", font=("Arial", 10), background=self.background_color)
            gpa_label = ttk.Label(info_frame, text=f"GPA: {gpa}", font=("Arial", 10), background=self.background_color)
            credit_label = ttk.Label(info_frame, text=f"Credits: {the_credits}", font=("Arial", 10),
                                     background=self.background_color)
            profile_button = ttk.Button(info_frame, text="Profile",
                                        command=lambda e=student_object, a=self.background_color:
                                        self.open_profile_screen(e, a))

            name_label.grid(row=0, column=0, sticky="ew", padx=50, pady=5)
            mod_label.grid(row=0, column=1, sticky="ew", ipadx=5)
            icr_label.grid(row=0, column=2, sticky="ew", ipadx=5)
            gpa_label.grid(row=0, column=3, sticky="ew", ipadx=5)
            credit_label.grid(row=0, column=4, sticky="ew", ipadx=5)
            profile_button.grid(row=0, column=5, sticky="e", ipadx=5)

    def open_profile_screen(self, student_object, background_color):
        profile_window = StudentProfileScreen(self.controller, student_object, background_color)
        profile_window.columnconfigure(0, weight=1)
        profile_window.mainloop()


# noinspection PyTypeChecker
class StudentProfileScreen(tk.Toplevel):
    def __init__(self, container, student_object, color):
        super().__init__(container)
        self.controller = container
        self.configure(background="#292929")
        # Variables
        student_name = student_object.get_full_name()
        student_id = student_object.get_student_id()
        the_mod = student_object.get_mod()
        the_icr = str(student_object.get_icr()) + "%"
        the_gpa = student_object.get_gpa()
        the_credits = student_object.get_credits()
        # Setup
        self.title(student_name)
        self.config(background=color, padx=30, pady=10)
        inner_frame = ttk.Frame(self)
        inner_frame.config(padding=20)
        inner_frame.grid(sticky="nsew")

        # Widgets
        full_name_title = ttk.Label(inner_frame, text=student_name, font=("Arial", 25), anchor="center")
        student_id_title = ttk.Label(inner_frame, text=student_id, font=("Arial", 15), anchor="center")
        mod_title = ttk.Label(inner_frame, text=the_mod, font=("Arial", 15), anchor="center")
        icr_info = ttk.Label(inner_frame, text=f"ICR: {the_icr}", anchor="center")
        gpa_info = ttk.Label(inner_frame, text=f"GPA: {the_gpa}", anchor="center")
        credit_info = ttk.Label(inner_frame, text=f"Credits: {the_credits}", anchor="center")
        agenda_button = ttk.Button(inner_frame, text="Agenda")

        # Layout
        full_name_title.grid(row=0, column=0, sticky="ew")
        student_id_title.grid(row=1, column=0, sticky="ew")
        mod_title.grid(row=2, column=0, sticky="ew")
        icr_info.grid(row=4, column=0, sticky="ew")
        gpa_info.grid(row=5, column=0, sticky="ew")
        credit_info.grid(row=6, column=0, sticky="ew")
        agenda_button.grid(row=7, column=0, ipadx=10, ipady=10)


# noinspection PyGlobalUndefined
class TodayBookingScreen(ttk.Frame):
    def __init__(self, container: RightSideFrame, list_of_bookings):
        super().__init__(container)
        global cancel_icon_image, check_icon_image

        self.check_icon_image = ImageTk.PhotoImage(Image.open(create_path('imgs/checkmark.png')).resize(size=(32, 32)))
        self.cancel_icon_image = ImageTk.PhotoImage(Image.open(create_path('imgs/cancel.png')).resize(size=(32, 32)))

        self.list_of_bookings = list_of_bookings
        self.controller = container
        self.supersaas_controller = self.controller.controller.supersaas_controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.the_frame = ttk.Frame(self, padding=20)
        self.the_frame.rowconfigure(0, weight=1)
        self.the_frame.columnconfigure(0, weight=1)

        self.the_canvas = tk.Canvas(self.the_frame, background="#292929")
        self.the_canvas.grid_columnconfigure(0, weight=1)

        self.scroll_bar = ttk.Scrollbar(self, orient="vertical", command=self.the_canvas.yview)

        self.scrollable_frame = ttk.Frame(self.the_canvas, padding=10)
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.the_canvas.configure(scrollregion=self.the_canvas.bbox("all")))
        self.scrollable_frame.columnconfigure(0, weight=1)

        self.the_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.the_canvas.config(yscrollcommand=self.scroll_bar.set)

        self.the_frame.grid(sticky="nsew")
        self.the_canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")

        self.show_list()

    # noinspection PyGlobalUndefined
    def show_list(self):
        for booking in self.list_of_bookings:
            booked_email = booking.__getattribute__("created_by")
            if booked_email.split(" ")[0].split("@")[1] != "sae.edu":
                student_id = booked_email.split(".")[0]
                booked_name = booking.__getattribute__("full_name")
                booked_room = booking.__getattribute__("res_name")
                booked_time = datetime.datetime.fromisoformat(booking.__getattribute__("start"))
                booked_time_format = booked_time.strftime("%I:%M%p")
                user_id = booking.__getattribute__("user_id")
                booking_id = booking.__getattribute__("id")
                status = self.supersaas_controller.get_database().get_booking_status_by_booking_id(booking_id)

                if status == "CLOSED":
                    background_color = "#00B0B9"
                elif status == "BLOCKED":
                    background_color = "#EE2737"
                else:
                    background_color = "#292929"

                label_style = status + ".TLabel"

                info_frame = tk.LabelFrame(self.scrollable_frame, background=background_color)
                self.grid_columnconfigure(0, weight=1)
                info_frame.grid(column=0, sticky="nsew", pady=5)
                info_frame.grid_columnconfigure(5, weight=1)
                info_frame.grid_columnconfigure(4, weight=1)

                name_label = ttk.Label(info_frame, text=booked_name, font=("Arial", 15), style=label_style)
                room_label = ttk.Label(info_frame, text=booked_room, font=("Arial", 20), style=label_style)
                time_label = ttk.Label(info_frame, text=booked_time_format, font=("Arial", 20), style=label_style)
                check_icon = ttk.Button(info_frame, image=self.check_icon_image, style="Title.TButton",
                                        command=lambda a=booking: self.checkmark_booking(a))
                cancel_icon = ttk.Button(info_frame, image=self.cancel_icon_image, style="Title.TButton",
                                         command=lambda a=student_id, e=user_id, c=booking:
                                         self.x_out_booking(a, e, c))

                name_label.grid(row=0, column=2, ipadx=5, pady=10)
                room_label.grid(row=0, column=0, ipadx=5)
                time_label.grid(row=0, column=1, ipadx=5)
                if status == "OPEN":
                    check_icon.grid(row=0, column=4, sticky="e", ipadx=5)
                    cancel_icon.grid(row=0, column=5, sticky="e", ipadx=5)

    def x_out_booking(self, student_id, user_id, booking):
        booking_id = booking.__getattribute__("id")
        self.controller.controller.supersaas_controller.block_student(student_id, user_id, booking)
        self.supersaas_controller.get_database().set_booking_status_by_booking_id(booking_id, "BLOCKED")
        self.controller.get_today_bookings()

    def checkmark_booking(self, booking):
        booking_id = booking.__getattribute__("id")
        self.supersaas_controller.get_database().set_booking_status_by_booking_id(booking_id, "CLOSED")
        self.controller.get_today_bookings()


if __name__ == "__main__":
    ss = SuperSaasController()
    app = App(ss)
    ss.set_app(app)
    app.mainloop()
