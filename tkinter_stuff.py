import time
import datetime
import tkinter as tk
from tkinter import ttk
from SuperSaasController import SuperSaasController
import webbrowser
from PIL import Image, ImageTk
from SettingsScreen import SettingsScreen
import sys
import os


class App(tk.Tk):
    def __init__(self, sscontrol: SuperSaasController):
        super().__init__()
        self.config(background="#292929")
        # Value Variables
        self.output_value = tk.StringVar()
        # Outside Objects
        self.supersaas_controller = sscontrol

        # Setup
        self.title("SAE NYC Booking Manager")
        # self.resizable(False, False)
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}")
        # self.attributes("-fullscreen", True)
        self.style = StyleClass(self)

        # Frames
        title_frame = TitleFrame(self)
        self.output_screen = OutputScreen(self)
        self.output_screen.columnconfigure(0, weight=1)
        self.buttons_frame = ButtonFrames(self)
        self.side_frame = SideFrame(self)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
        self.side_frame.grid(row=1, column=2, rowspan=2, sticky="ew")
        self.output_screen.grid(row=1, column=0, columnspan=3, sticky="new")
        self.buttons_frame.grid(row=2, column=0, sticky="new")

        self.print_output("Welcome to SAE NYC Booking Manager.")

    def print_output(self, output_text):
        self.output_screen.print_output(output_text)


class StyleClass(ttk.Style):
    def __init__(self, container: App):
        super().__init__(container)

        background_white = "#FFFFFF"
        background_dark = "#292929"
        # sae_blue = "#307FE2"
        # sae_teal = "#00B0B9"
        # sae_red = "#EE2737"
        # sae_yellow = "#FFB500"
        # sae_light_blue = "#58c9e6"

        self.theme_use("default")
        # Test Stuff
        self.configure("Red.TFrame", background="red")
        self.configure("Blue.TFrame", background="blue")

        self.configure("TFrame", background=background_dark)
        self.configure("TLabel", background=background_dark, foreground="white")
        self.configure("TButton", background=background_white, foreground=background_dark,
                       relief="solid", borderwidth=2, padding=0)
        self.configure("Title.TButton", background=background_dark, relief="flat")
        self.configure("Big.TButton", background=background_white, font=("Arial", 25),
                       foreground=background_dark, relief="solid", borderwidth=2)


# noinspection PyGlobalUndefined,PyTypeChecker
class TitleFrame(ttk.Frame):
    def __init__(self, container: App):
        super().__init__(container)
        global logo, settings_icon_image, web_icon_image, refresh_icon_image

        self.controller = container
        # Variables
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_to_logo = os.path.abspath(os.path.join(bundle_dir, 'imgs/Transparent Smaller.png'))
        logo = ImageTk.PhotoImage(Image.open(path_to_logo).resize(size=(128, 128)))
        path_to_settings_icon = os.path.abspath(os.path.join(bundle_dir, 'imgs/settings.png'))
        settings_icon_image = ImageTk.PhotoImage(Image.open(path_to_settings_icon).resize(size=(64, 64)))
        path_to_web_icon = os.path.abspath(os.path.join(bundle_dir, 'imgs/internet.png'))
        web_icon_image = ImageTk.PhotoImage(Image.open(path_to_web_icon).resize(size=(64, 64)))
        path_to_refresh_icon = os.path.abspath(os.path.join(bundle_dir, 'imgs/refresh.png'))
        refresh_icon_image = ImageTk.PhotoImage(Image.open(path_to_refresh_icon).resize(size=(64, 64)))

        # Widgets
        logo_label = ttk.Label(self, image=logo, padding=(50, 0, 50, 0))
        title_label = ttk.Label(self, text="SAE NYC Booking Manager", foreground="White", font=("Arial", 35))

        info_frame = ttk.Frame(self)
        button_frame = ttk.Frame(self)

        settings_icon = ttk.Button(button_frame, image=settings_icon_image,
                                   command=self.open_settings_page, style="Title.TButton")
        web_icon = ttk.Button(button_frame, image=web_icon_image, command=self.open_web_pages, style="Title.TButton")
        refresh_icon = ttk.Button(button_frame, image=refresh_icon_image,
                                  command=self.get_all_info, style="Title.TButton")

        seperator = ttk.Separator(self, orient="horizontal")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Layout
        logo_label.grid(row=0, column=0, sticky="e")
        title_label.grid(row=0, column=1, sticky="w")

        info_frame.grid(row=0, column=2, sticky="ew")

        button_frame.grid(row=0, column=3, sticky="ew")
        settings_icon.grid(row=0, column=0, padx=5)
        web_icon.grid(row=0, column=1, padx=5)
        refresh_icon.grid(row=0, column=2, padx=5)

        seperator.grid(row=1, column=0, columnspan=5, sticky="ew")

    def open_settings_page(self):
        settings_page = SettingsScreen(self.controller)
        settings_page.mainloop()

    def open_web_pages(self):
        webbrowser.open(
            "https://docs.google.com/spreadsheets/d/17IIW21BzwSirT5g53Un9oYEZUSB0CaRmS55f9ur8n94/edit#gid=1026026296")
        webbrowser.open("https://supersaas.com/schedule/SAE_New_York/5th_Floor_Booking")
        self.controller.print_output("Web pages open")

    def get_all_info(self):
        start_time = time.perf_counter()
        self.controller.supersaas_controller.get_all_info()
        end_time = time.perf_counter() - start_time
        self.controller.print_output(f"Retrieved all student info in {end_time:.2f} seconds")
        self.controller.print_output(f"Current: {self.get_number_of_users()} Users {self.get_number_of_bookings()} Bookings")
        button_frame = self.controller.buttons_frame
        for button in button_frame.winfo_children():
            button_frame.set_button_states(button)

    def get_number_of_users(self):
        user_num = self.controller.supersaas_controller.get_number_of_current_users()
        return user_num

    def get_number_of_bookings(self):
        booking_num = self.controller.supersaas_controller.get_number_of_current_bookings()
        return booking_num


class SideFrame(ttk.Frame):
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

        today_bookings_button.grid(row=0, column=0, sticky="ew", padx=10, pady=10, ipady=10)
        student_list_button.grid(row=0, column=1, sticky="ew", padx=10, pady=10, ipady=10)

        self.student_list_page = None
        self.today_booking_screen = None

        self.open_student_list_page()

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
        self.student_list_page.columnconfigure(0, weight=1)
        self.student_list_page.rowconfigure(0, weight=1)


class OutputScreen(ttk.Frame):
    def __init__(self, container: App):
        super().__init__(container)
        self.screen = tk.Text(self, state="disabled", background="black", foreground="white",
                              font=("Arial", 15), wrap="word")
        self.screen.grid(sticky="nsew")

    def print_output(self, output_text):
        self.screen.config(state="normal")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        final_output = f"{current_time}: {output_text}\n"
        self.screen.insert("1.0", final_output)
        self.screen.config(state="disabled")


# noinspection PyTypeChecker
class ButtonFrames(ttk.Frame):
    def __init__(self, container: App):
        super().__init__(container)
        self.controller = container

        self.configure(style="Red.TFrame")
        # Buttons
        go_through_users_button = ttk.Button(self, text="Go Through Users",
                                             command=self.go_through_all_users, style="Big.TButton")
        go_through_bookings_button = ttk.Button(self, text="Go Through Bookings",
                                                command=self.go_through_all_bookings, style="Big.TButton")
        teacher_booking_button = ttk.Button(self, text="Teacher Booking",
                                            command=self.open_teacher_booking_page, style="Big.TButton")
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        go_through_users_button.grid(row=0, column=0, sticky="ew", padx=10, pady=10, ipady=10)
        go_through_bookings_button.grid(row=1, column=0, sticky="ew", padx=10, pady=10, ipady=10)
        teacher_booking_button.grid(row=0, column=2, sticky="ew", padx=10, pady=10, ipady=10)

        for button in self.winfo_children():
            self.set_button_states(button)

    def set_button_states(self, button):
        if not self.controller.supersaas_controller.info_is_there():
            button['state'] = "disabled"
        else:
            button['state'] = "normal"

    def go_through_all_users(self):
        start_time = time.perf_counter()
        self.controller.supersaas_controller.go_through_all_users()
        end_time = time.perf_counter() - start_time
        num_changes = self.controller.supersaas_controller.get_number_of_changes()
        self.controller.print_output(f"Done Processing Users - {num_changes} changes. - {end_time:.2f} seconds")

    def go_through_all_bookings(self):
        start_time = time.perf_counter()
        self.controller.supersaas_controller.go_through_all_bookings()
        end_time = time.perf_counter() - start_time
        num_changes = self.controller.supersaas_controller.get_number_of_changes()
        self.controller.print_output(f"Done Sorting Bookings - {num_changes} changes. - {end_time:.2f} seconds")

    def open_teacher_booking_page(self):
        teacher_booking_page = TeacherBookingScreen(self.controller)
        teacher_booking_page.mainloop()


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
    def __init__(self, container: SideFrame):
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
                                        command=lambda e=student_object, a=self.background_color: self.open_profile_screen(e, a))

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
        the_class_schedule = student_object.get_class_schedule()
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
        class_schedule_title = ttk.Label(inner_frame, text=the_class_schedule, font=("Arial", 15), anchor="center")
        icr_info = ttk.Label(inner_frame, text=f"ICR: {the_icr}", anchor="center")
        gpa_info = ttk.Label(inner_frame, text=f"GPA: {the_gpa}", anchor="center")
        credit_info = ttk.Label(inner_frame, text=f"Credits: {the_credits}", anchor="center")
        agenda_button = ttk.Button(inner_frame, text="Agenda")

        # Layout
        full_name_title.grid(row=0, column=0, sticky="ew")
        student_id_title.grid(row=1, column=0, sticky="ew")
        mod_title.grid(row=2, column=0, sticky="ew")
        class_schedule_title.grid(row=3, column=0, sticky="ew")
        icr_info.grid(row=4, column=0, sticky="ew")
        gpa_info.grid(row=5, column=0, sticky="ew")
        credit_info.grid(row=6, column=0, sticky="ew")
        agenda_button.grid(row=7, column=0, ipadx=10, ipady=10)


# noinspection PyGlobalUndefined
class TodayBookingScreen(ttk.Frame):
    def __init__(self, container: SideFrame, list_of_bookings):
        super().__init__(container)
        global cancel_icon_image, check_icon_image
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_to_check_icon = os.path.abspath(os.path.join(bundle_dir, 'imgs/checkmark.png'))
        self.check_icon_image = ImageTk.PhotoImage(Image.open(path_to_check_icon).resize(size=(32, 32)))
        path_to_cancel_icon = os.path.abspath(os.path.join(bundle_dir, 'imgs/cancel.png'))
        self.cancel_icon_image = ImageTk.PhotoImage(Image.open(path_to_cancel_icon).resize(size=(32, 32)))

        self.list_of_bookings = list_of_bookings
        self.background_color = None
        self.controller = container
        self.columnconfigure(0, weight=1)

        self.the_frame = tk.Frame(self)
        self.the_frame.rowconfigure(0, weight=1)
        self.the_frame.columnconfigure(0, weight=1)

        self.the_canvas = tk.Canvas(self.the_frame, height=self.controller.controller.height, background="#292929")

        self.scroll_bar = ttk.Scrollbar(self, orient="vertical", command=self.the_canvas.yview)

        self.scrollable_frame = ttk.Frame(self.the_canvas, padding=10)
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.the_canvas.configure(scrollregion=self.the_canvas.bbox("all")))
        self.scrollable_frame.columnconfigure(0, weight=1)

        self.the_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.the_canvas.config(yscrollcommand=self.scroll_bar.set)

        self.the_frame.grid(sticky="nsew")
        self.the_canvas.grid(sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")

        self.show_list()

    # noinspection PyGlobalUndefined
    def show_list(self):
        for booking in self.list_of_bookings:
            booked_name = booking.__getattribute__("full_name")
            booked_mod = booking.__getattribute__("field_1_r")
            booked_room = booking.__getattribute__("res_name")
            booked_time = datetime.datetime.fromisoformat(booking.__getattribute__("start")).strftime("%I:%M%p")
            user_id = booking.__getattribute__("user_id")
            booking_id = booking.__getattribute__("id")

            info_frame = tk.LabelFrame(self.scrollable_frame, background="#292929")
            info_frame.grid(sticky="ew", pady=5)

            name_label = ttk.Label(info_frame, text=booked_name, font=("Arial", 15), background=self.background_color)
            mod_label = ttk.Label(info_frame, text=booked_mod, font=("Arial", 10), background=self.background_color)
            room_label = ttk.Label(info_frame, text=booked_room, font=("Arial", 10), background=self.background_color)
            time_label = ttk.Label(info_frame, text=booked_time, font=("Arial", 10), background=self.background_color)

            check_icon = ttk.Button(info_frame, image=self.check_icon_image, style="Title.TButton")
            cancel_icon = ttk.Button(info_frame, image=self.cancel_icon_image, style="Title.TButton",
                                     command=lambda a=booking_id, e=user_id: self.x_out_booking(a, e))

            # for i in range(6):
            #     self.grid_columnconfigure(i, weight=1)

            name_label.grid(row=0, column=0, sticky="ew", padx=50, pady=5)
            mod_label.grid(row=0, column=1, sticky="ew", ipadx=5)
            room_label.grid(row=0, column=2, sticky="ew", ipadx=5)
            time_label.grid(row=0, column=3, sticky="ew", ipadx=5)
            check_icon.grid(row=0, column=4, sticky="e", ipadx=5)
            cancel_icon.grid(row=0, column=5, sticky="e", ipadx=5)

    @staticmethod
    def x_out_booking(booking_id, user_id):
        print(f"{booking_id} by {user_id} has missed their booking")

    @staticmethod
    def checkmark_booking(booking_id, user_id):
        print(f"{booking_id} by {user_id} has missed their booking")


if __name__ == "__main__":
    ss = SuperSaasController()
    app = App(ss)
    ss.set_app(app)
    app.mainloop()
