
from tkinter.font import Font
from DriverAssignmentManagement import DriverAssignmentManagement
from DriverManagement import DriverManagement
from QueriesFunctionsWindow import QueriesFunctionsWindow
from ScheduleManagement import ScheduleManagement
from StaffManagement import StaffManagement
import tkinter as tk

class MainApplication:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.title("Staff Management System - Main Menu")
        self.root.geometry("800x600")
        self.root.configure(bg='#f8f0fc')
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_font = Font(family="Arial", size=26, weight="bold")
        title_label = tk.Label(self.root, text="Staff Management System",
                               font=title_font, bg='#f8f0fc', fg='#4b3f72')
        title_label.pack(pady=40)

        # Button frame
        button_frame = tk.Frame(self.root, bg='#f8f0fc')
        button_frame.pack(pady=10)

        pastel_colors = ['#a2d2ff', '#cdb4db','#ffc9de','#b5ead7','#fdffb6']

        # Buttons: alternating between pastels
        buttons = [
            ("Staff Management", self.open_staff_management),
            ("Schedule Management", self.open_schedule_management),
            ("Driver Assignment", self.open_driver_assignment),
            ("Driver Management", self.open_driver_management),
            ("Queries & Reports", self.open_queries),
            ("Exit", self.exit_app)
        ]

        for i, (text, command) in enumerate(buttons):
            color = pastel_colors[i % 5]
            btn = tk.Button(button_frame, text=text, command=command,
                            bg=color, fg='black', activebackground=color,
                            font=('Arial', 14, 'bold'),
                            width=25, height=2, bd=0, relief='ridge')
            btn.pack(pady=12)

    def open_staff_management(self):
        StaffManagement(self.root, self.db)

    def open_schedule_management(self):
        ScheduleManagement(self.root, self.db)

    def open_driver_assignment(self):
        DriverAssignmentManagement(self.root, self.db)

    def open_driver_management(self):
        DriverManagement(self.root, self.db)

    def open_queries(self):
        QueriesFunctionsWindow(self.root, self.db)

    def exit_app(self):
        self.db.disconnect()
        self.root.quit()

    def run(self):
        self.root.mainloop()

