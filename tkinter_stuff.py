import time
import datetime
import tkinter as tk
from tkinter import ttk
from SuperSaasController import SuperSaasController
import webbrowser


class App(tk.Tk):
    def __init__(self, sscontrol):
        super().__init__()
        # Display Variables
        self.background_color = "#292929"
        # Value Variables
        self.output_value = tk.StringVar()
        # Outside Objects
        self.supersaas_controller = sscontrol
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
        # title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        # title_frame.columnconfigure(0, weight=1)
        # title_frame.rowconfigure(0, weight=1)
        self.output_screen.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        self.print_output("Welcome to SAE NYC Booking Manager.")

    def print_output(self, output_text):
        self.output_screen.print_output(output_text)


class TitleFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Widgets
        title = ttk.Label(self,
                          text="SAE NYC Booking Manager", background="black",
                          foreground="white",
                          font=("Arial", 15)
                          )

        # Layout
        title.grid(column=0, row=1, columnspan=2, sticky="ew")


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
        print(self.controller)
        # Buttons
        get_number_users_button = ttk.Button(self, text="Get # of Users", command=self.get_number_of_users)
        go_through_users_button = ttk.Button(self, text="Go Through Users", command=self.go_through_all_users)
        get_number_of_bookings_button = ttk.Button(self, text="Get # of Bookings", command=self.get_number_of_bookings)
        go_through_bookings_button = ttk.Button(self, text="Go Through Bookings", command=self.go_through_all_bookings)
        get_info_button = ttk.Button(self, text="Get All Info", command=self.get_all_info)
        open_web_pages_button = ttk.Button(self, text="Open Web Pages", command=self.open_web_pages)
        # Layout
        get_number_users_button.grid(row=0, column=0, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        go_through_users_button.grid(row=0, column=1, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        get_number_of_bookings_button.grid(row=1, column=0, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        go_through_bookings_button.grid(row=1, column=1, sticky="ew", ipady=10, ipadx=10, pady=5, padx=5)
        get_info_button.grid(row=2, column=0, columnspan=2, sticky="ew")
        open_web_pages_button.grid(row=3, column=0, columnspan=2)

        for button in self.winfo_children():
            self.set_button_states(button)
        get_info_button['state'] = "normal"
        open_web_pages_button['state'] = "normal"

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


sscontrol = SuperSaasController()
app = App(sscontrol)
sscontrol.set_app(app)
app.mainloop()
