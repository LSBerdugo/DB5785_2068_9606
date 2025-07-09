import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class ScheduleManagement:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Schedule Management")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f8f0fc')
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        # Fonts that say "I'm professional but also chill"
        title_font = Font(family="Segoe UI", size=22, weight="bold")
        label_font = ('Segoe UI', 12)
        btn_font = ('Segoe UI', 10, 'bold')

        # Title Label
        title = tk.Label(self.window, text="📅 Schedule Management",
                         font=title_font, bg='white', fg='#4b3f72')
        title.pack(pady=15)

        # Form Area
        form_frame = tk.LabelFrame(self.window, text="Schedule Information",
                                   font=('Segoe UI', 14, 'bold'),
                                   bg='white', fg='#4b3f72', bd=2, relief='groove')
        form_frame.pack(padx=20, pady=10, fill='x')

        self.entries = {}
        fields = ["ScheduleID", "ShiftStart", "ShiftEnd", "StaffID"]
        for i, field in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            label = tk.Label(form_frame, text=f"{field}:", bg='white',
                             fg='#4b3f72', font=label_font)
            label.grid(row=row, column=col, sticky='e', padx=10, pady=8)

            entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30,
                             highlightbackground='#d0bdf4', highlightcolor='#d0bdf4',
                             relief='solid', bd=1)
            entry.grid(row=row, column=col+1, padx=10, pady=8)
            self.entries[field] = entry

        help_text = tk.Label(form_frame, text="Format for time: YYYY-MM-DD HH:MM:SS",
                             bg='white', fg='#888', font=('Segoe UI', 9, 'italic'))
        help_text.grid(row=2, column=0, columnspan=4, pady=(0, 10))

        # Buttons that slap
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        buttons = [
            ("➕ Add", self.add_schedule, '#a2d2ff'),
            ("📝 Update", self.update_schedule, '#cdb4db'),
            ("❌ Delete", self.delete_schedule, '#ffc9de'),
            ("🧹 Clear", self.clear_form, '#b5ead7'),
            ("🔍 Select", self.select_schedule, '#fdffb6')
        ]

        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                            font=btn_font, bg=color, fg='black',
                            width=14, height=2, bd=0, relief='ridge',
                            activebackground=color, cursor="hand2")
            btn.pack(side='left', padx=8)

        # Table area
        list_frame = tk.LabelFrame(self.window, text="📋 Schedule List",
                                   font=('Segoe UI', 14, 'bold'),
                                   bg='white', fg='#4b3f72')
        list_frame.pack(padx=20, pady=10, fill='both', expand=True)

        columns = ("Schedule ID", "Shift Start", "Shift End", "Staff ID", "Staff Name")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=28, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'), foreground='#4b3f72')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor='center')

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.on_item_select)

    def add_schedule(self):
        try:
            data = self.get_form_data()
            query = """INSERT INTO Schedule (ShiftStart, ShiftEnd, StaffID) 
                          VALUES (%s, %s, %s)"""
            self.db.cursor.execute(query, data[1:])
            self.db.connection.commit()
            messagebox.showinfo("Success", "Schedule added successfully!")
            self.clear_form()
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add schedule: {str(e)}")

    def update_schedule(self):
        try:
            data = self.get_form_data()
            query = """UPDATE Schedule SET ShiftStart=%s, ShiftEnd=%s, StaffID=%s 
                          WHERE ScheduleID=%s"""
            self.db.cursor.execute(query, data[1:] + (data[0],))
            self.db.connection.commit()
            messagebox.showinfo("Success", "Schedule updated successfully!")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update schedule: {str(e)}")

    def delete_schedule(self):
        try:
            schedule_id = self.entries["ScheduleID"].get()
            if not schedule_id:
                messagebox.showwarning("Warning", "enter a Schedule ID to delete")
                return

            if messagebox.askyesno("Confirm", "Are you you want to delete this schedule?"):
                query = "DELETE FROM Schedule WHERE ScheduleID=%s"
                self.db.cursor.execute(query, (schedule_id,))
                self.db.connection.commit()
                messagebox.showinfo("Success", "Schedule deleted successfully!")
                self.clear_form()
                self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting schedule: {str(e)}")

    def get_form_data(self):
        return tuple(self.entries[field].get() for field in
                     ["ScheduleID", "ShiftStart", "ShiftEnd", "StaffID"])

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            query = """SELECT s.ScheduleID, s.ShiftStart, s.ShiftEnd, s.StaffID, 
                          CONCAT(st.First_Name, ' ', st.Last_Name) as staff_name
                          FROM Schedule s 
                          JOIN Staff st ON s.StaffID = st.StaffID 
                          ORDER BY s.ScheduleID"""
            self.db.cursor.execute(query)
            for row in self.db.cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch schedule data: {str(e)}")

    def on_item_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            fields = ["ScheduleID", "ShiftStart", "ShiftEnd", "StaffID"]
            for i, field in enumerate(fields):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, values[i])

    def select_schedule(self):
        try:
            schedule_id = self.entries["ScheduleID"].get()
            if not schedule_id:
                messagebox.showwarning("Input Required", "Please enter a Schedule ID to select.")
                return

            query = """SELECT s.ScheduleID, s.ShiftStart, s.ShiftEnd, s.StaffID,
                          CONCAT(st.First_Name, ' ', st.Last_Name)
                   FROM Schedule s
                   JOIN Staff st ON s.StaffID = st.StaffID
                   WHERE s.ScheduleID = %s"""
            self.db.cursor.execute(query, (schedule_id,))
            result = self.db.cursor.fetchone()

            if result:
                fields = ["ScheduleID", "ShiftStart", "ShiftEnd", "StaffID"]
                for i, field in enumerate(fields):
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, result[i])

                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == int(schedule_id):
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break
            else:
                messagebox.showinfo("Not Found", "That Schedule ID does not exist")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to select schedule: {str(e)}")
