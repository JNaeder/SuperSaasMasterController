import time
import datetime
import tkinter as tk
from tkinter import ttk
from SuperSaasController import SuperSaasController
import webbrowser
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self, sscontrol):
        super().__init__()
        # Display Variables
        self.background_color = "#292929"
        # Value Variables
        self.output_value = tk.StringVar()
        # Outside Objects
        self.supersaas_controller = sscontrol
        # Style
        style = ttk.Style(self)
        # print(style.theme_names())
        style.theme_use("default")
        # print(style.theme_use())
        style.configure("TFrame", background=self.background_color)
        # style.configure("TButton", background=self.background_color, font=("Arial", 12))
        style.configure("TLabel", background=self.background_color, foreground="white")
        style.configure("TCheckbutton", background=self.background_color, foreground="white")
        # print(style.layout("TCheckbutton"))
        # print(style.element_options("Checkbutton.label"))
        # print(style.lookup("TCheckbutton", "text"))
        # Setup
        self.title("SAE NYC Booking Manager")
        self.resizable(False, False)
        self.config(background=self.background_color)
        # Frames
        title_frame = TitleFrame(self)
        self.output_screen = OutputScreen(self)
        self.output_screen.columnconfigure(0, weight=1)
        buttons_frame = ButtonFrames(self)
        # Layouts
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        title_frame.columnconfigure(1, weight=1)
        title_frame.columnconfigure(0, weight=1)
        self.output_screen.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        # buttons_frame.columnconfigure(0, weight=1)
        # buttons_frame.columnconfigure(1, weight=1)

        self.print_output("Welcome to SAE NYC Booking Manager.")

    def print_output(self, output_text):
        self.output_screen.print_output(output_text)


class TitleFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        global logo
        # Variables
        logo = ImageTk.PhotoImage(Image.open("imgs/Transparent Smaller.png").resize(size=(128, 128)))

        # Widgets
        logo_label = ttk.Label(self, image=logo, background=container.background_color, padding=(50, 0, 50, 0))
        title_label = ttk.Label(self, text="SAE NYC Booking Manager", foreground="White", font=("Arial", 35))

        # Layout
        logo_label.grid(row=0, column=0)
        title_label.grid(row=0, column=1, sticky="ew")


class OutputScreen(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.screen = tk.Text(self, height=20, width=100, background=container.background_color, state="disabled",
                              font=("Arial", 15), foreground="white", wrap="word")
        self.screen.grid(sticky="ew")

    def print_output(self, output_text):
        self.screen.config(state="normal")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        final_output = f"{current_time}: {output_text}\n"
        self.screen.insert("1.0", final_output)
        self.screen.config(state="disabled")


class ButtonFrames(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.controller = container
        # Buttons
        get_number_users_button = ttk.Button(self, text="Get # of Users", command=self.get_number_of_users)
        go_through_users_button = ttk.Button(self, text="Go Through Users", command=self.go_through_all_users)
        get_number_of_bookings_button = ttk.Button(self, text="Get # of Bookings", command=self.get_number_of_bookings)
        go_through_bookings_button = ttk.Button(self, text="Go Through Bookings", command=self.go_through_all_bookings)
        get_info_button = ttk.Button(self, text="Get All Info", command=self.get_all_info)
        open_web_pages_button = ttk.Button(self, text="Open Web Pages", command=self.open_web_pages)
        teacher_booking_button = ttk.Button(self, text="Teacher Booking", command=self.open_teacher_booking_page)
        student_list_button = ttk.Button(self, text="Student List", command=self.open_student_list_page)
        # Layout
        get_number_users_button.grid(row=0, column=0, columnspan=2, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        go_through_users_button.grid(row=0, column=2, columnspan=2, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        get_number_of_bookings_button.grid(row=1, column=0, columnspan=2, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        go_through_bookings_button.grid(row=1, column=2, columnspan=2, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)

        get_info_button.grid(row=2, column=1, ipadx=50, ipady=5, sticky="ew", padx=5, pady=5)
        open_web_pages_button.grid(row=2, column=2, ipadx=50, ipady=5, sticky="ew", padx=5, pady=5)
        teacher_booking_button.grid(row=3, column=1, ipadx=50, ipady=5, sticky="ew", padx=5, pady=5)
        student_list_button.grid(row=3, column=2, ipadx=50, ipady=5, sticky="ew", padx=5, pady=5)

        for button in self.winfo_children():
            self.set_button_states(button)
        get_info_button['state'] = "normal"
        open_web_pages_button['state'] = "normal"
        student_list_button['state'] = "normal"

    def set_button_states(self, button):
        if not self.controller.supersaas_controller.info_is_there():
            button['state'] = "disabled"
        else:
            button['state'] = "normal"

    def get_number_of_users(self):
        start_time = time.perf_counter()
        user_num = self.controller.supersaas_controller.get_number_of_current_users()
        end_time = time.perf_counter() - start_time
        self.controller.print_output(f"There are {str(user_num)} current Users. - {end_time:.2f} seconds")

    def go_through_all_users(self):
        start_time = time.perf_counter()
        self.controller.supersaas_controller.go_through_all_users()
        end_time = time.perf_counter() - start_time
        num_changes = self.controller.supersaas_controller.get_number_of_changes()
        self.controller.print_output(f"Done Processing Users - {num_changes} changes. - {end_time:.2f} seconds")

    def get_number_of_bookings(self):
        start_time = time.perf_counter()
        booking_num = self.controller.supersaas_controller.get_number_of_current_bookings()
        end_time = time.perf_counter() - start_time
        self.controller.print_output(f"There are {booking_num} current bookings. - {end_time:.2f} seconds")

    def go_through_all_bookings(self):
        start_time = time.perf_counter()
        self.controller.supersaas_controller.go_through_all_bookings()
        end_time = time.perf_counter() - start_time
        num_changes = self.controller.supersaas_controller.get_number_of_changes()
        self.controller.print_output(f"Done Sorting Bookings - {num_changes} changes. - {end_time:.2f} seconds")

    def get_all_info(self):
        start_time = time.perf_counter()
        self.controller.supersaas_controller.get_all_info()
        end_time = time.perf_counter() - start_time
        self.controller.print_output(f"Retrieved all student info in {end_time:.2f} seconds")
        for button in self.winfo_children():
            self.set_button_states(button)

    def open_web_pages(self):
        webbrowser.open(
            "https://docs.google.com/spreadsheets/d/17IIW21BzwSirT5g53Un9oYEZUSB0CaRmS55f9ur8n94/edit#gid=1026026296")
        webbrowser.open("https://supersaas.com/schedule/SAE_New_York/5th_Floor_Booking")
        self.controller.print_output("Web pages open")

    def open_teacher_booking_page(self):
        teacher_booking_page = TeacherBookingScreen(self.controller)
        teacher_booking_page.mainloop()

    def open_student_list_page(self):
        student_list_page = StudentListScreen(self.controller)
        student_list_page.mainloop()


class TeacherBookingScreen(tk.Toplevel):
    def __init__(self, container):
        super().__init__(container)
        self.controller = container

        # Text Variables
        self.name_selection_var = tk.StringVar()
        self.mod_selection_var = tk.StringVar()
        self.studio_selection_var = tk.StringVar()
        self.time_start_var = tk.StringVar()
        self.time_length_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        # Setup
        self.title("Teacher Booking")
        self.config(background=self.controller.background_color, padx=50, pady=50)
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
        studio_selection['values'] = ("SSL", "Audient", "Avid S6", "02R", "Production Suite 1", "Production Suite 2",
                                      "Production Suite 3", "Production Suite 4")
        time_start_label = ttk.Label(self, text="Start Time: ")
        time_start_entry = ttk.Entry(self, textvariable=self.time_start_var)
        time_length_label = ttk.Label(self, text="Booking Length: ")
        time_length_entry = ttk.Entry(self, textvariable=self.time_length_var)
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
        time_length_label.grid(row=4, column=0)
        time_length_entry.grid(row=4, column=1)
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
        start_time = int(self.time_start_var.get())
        length_time = int(self.time_length_var.get())
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        self.controller.supersaas_controller.set_repeating_bookings(the_name, the_mod, the_studio, start_time,
                                                                    length_time, start_date, end_date)
        self.controller.print_output(f"Booked {the_studio} for {the_name}, from {start_date} to {end_date}")
        self.destroy()


class StudentListScreen(tk.Toplevel):
    def __init__(self, container):
        super().__init__(container)
        self.controller = container
        self.title("Student List")
        self.geometry("600x400")
        self.config(background=self.controller.background_color)

        self.the_frame = tk.Frame(self, background="red")
        self.the_canvas = tk.Canvas(self.the_frame, background="green")
        self.the_canvas.columnconfigure(0, weight=1)

        self.the_frame.grid(sticky="nsew")
        self.the_canvas.grid(sticky="nsew")

        self.show_list()


    def show_list(self):
        list_of_students = self.controller.supersaas_controller.get_student_holder().get_list_of_student_objects()
        for index in range(len(list_of_students)):
            student_object = list_of_students[index]
            full_name = student_object.get_full_name()
            mod = student_object.get_mod()
            new_student_label = ttk.Label(self.the_canvas, text=full_name + " " + mod)
            new_student_label.grid(row=index, column=0, sticky="ew", padx=50)


if __name__ == "__main__":
    ss = SuperSaasController()
    app = App(ss)
    ss.set_app(app)
    app.mainloop()
