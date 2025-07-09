import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class DriverAssignmentManagement:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Driver Assignment Management")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f8f0fc')
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        title_font = Font(family="Segoe UI", size=22, weight="bold")
        label_font = ('Segoe UI', 12)
        btn_font = ('Segoe UI', 10, 'bold')

        title = tk.Label(self.window, text="🚌 Driver Assignment Management",
                         font=title_font, bg='white', fg='#4b3f72')
        title.pack(pady=15)

        form_frame = tk.LabelFrame(self.window, text="Assignment Information",
                                   font=('Segoe UI', 14, 'bold'),
                                   bg='white', fg='#4b3f72', bd=2, relief='groove')
        form_frame.pack(padx=20, pady=10, fill='x')

        self.entries = {}
        fields = ["AssignmentID", "BusID", "AssignmentDate", "EndDate"]
        for i, field in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            label = tk.Label(form_frame, text=f"{field.replace('_', ' ')}:", bg='white',
                             fg='#4b3f72', font=label_font)
            label.grid(row=row, column=col, sticky='e', padx=10, pady=8)

            entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=30,
                             highlightbackground='#d0bdf4', highlightcolor='#d0bdf4',
                             relief='solid', bd=1)
            entry.grid(row=row, column=col+1, padx=10, pady=8)
            self.entries[field] = entry

        tk.Label(form_frame, text="Driver:", font=label_font,
                 bg='white', fg='#4b3f72').grid(row=2, column=0, sticky='e', padx=10, pady=8)
        self.driver_combo = ttk.Combobox(form_frame, width=28, state="readonly", font=('Segoe UI', 11))
        self.driver_combo.grid(row=2, column=1, padx=10, pady=8)
        self.driver_map = {}
        self.populate_driver_combo()

        help_text = tk.Label(form_frame, text="Date format: YYYY-MM-DD",
                             bg='white', fg='#888', font=('Segoe UI', 9, 'italic'))
        help_text.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10)

        buttons = [
            ("➕ Add", self.add_assignment, '#a2d2ff'),
            ("📝 Update", self.update_assignment, '#cdb4db'),
            ("❌ Delete", self.delete_assignment, '#ffc9de'),
            ("🧹 Clear", self.clear_form, '#b5ead7'),
            ("🔍 Select", self.select_assignment, '#fdffb6')
        ]

        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                            font=btn_font, bg=color, fg='black',
                            width=14, height=2, bd=0, relief='ridge',
                            activebackground=color, cursor="hand2")
            btn.pack(side='left', padx=8)

        list_frame = tk.LabelFrame(self.window, text="📋 Assignment List",
                                   font=('Segoe UI', 14, 'bold'),
                                   bg='white', fg='#4b3f72')
        list_frame.pack(padx=20, pady=10, fill='both', expand=True)

        columns = ("Assignment ID", "Bus ID", "Assignment Date", "End Date", "Staff ID", "Driver Name")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=28, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'), foreground='#4b3f72')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor='center')

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.on_item_select)

    def populate_driver_combo(self):
        try:
            self.db.cursor.execute("""
                SELECT s.StaffID, CONCAT(s.First_Name, ' ', s.Last_Name) 
                FROM Staff s 
                JOIN Driver d ON s.StaffID = d.StaffID
            """)
            drivers = self.db.cursor.fetchall()
            self.driver_map = {f"{name} (ID: {staff_id})": staff_id for staff_id, name in drivers}
            self.driver_combo['values'] = list(self.driver_map.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load drivers: {str(e)}")

    def get_form_data(self):
        staff_display = self.driver_combo.get()
        staff_id = self.driver_map.get(staff_display, "")
        return (
            self.entries["AssignmentID"].get(),
            self.entries["BusID"].get(),
            self.entries["AssignmentDate"].get(),
            self.entries["EndDate"].get(),
            staff_id
        )

    def add_assignment(self):
        try:
            data = list(self.get_form_data())
            if data[3] == "":
                data[3] = None
            query = """INSERT INTO DriverAssignment (BusID, AssignmentDate, EndDate, StaffID) 
                          VALUES (%s, %s, %s, %s)"""
            self.db.cursor.execute(query, data[1:])
            self.db.connection.commit()
            messagebox.showinfo("Success", "Driver assignment added successfully!")
            self.clear_form()
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add assignment: {str(e)}")

    def update_assignment(self):
        try:
            data = list(self.get_form_data())
            if data[3] == "":
                data[3] = None
            query = """UPDATE DriverAssignment SET BusID=%s, AssignmentDate=%s, 
                          EndDate=%s, StaffID=%s WHERE AssignmentID=%s"""
            self.db.cursor.execute(query, data[1:] + [data[0]])
            self.db.connection.commit()
            messagebox.showinfo("Success", "Driver assignment updated successfully!")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update assignment: {str(e)}")

    def delete_assignment(self):
        try:
            assignment_id = self.entries["AssignmentID"].get()
            if not assignment_id:
                messagebox.showwarning("Warning", "enter an Assignment ID to delete")
                return
            if messagebox.askyesno("Confirm", "Are you you want to delete this schedule?"):
                query = "DELETE FROM DriverAssignment WHERE AssignmentID=%s"
                self.db.cursor.execute(query, (assignment_id,))
                self.db.connection.commit()
                messagebox.showinfo("Success", "Assignment deleted successfully!")
                self.clear_form()
                self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete assignment: {str(e)}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.driver_combo.set("")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            query = """SELECT da.AssignmentID, da.BusID, da.AssignmentDate, 
                          da.EndDate, da.StaffID, CONCAT(s.First_Name, ' ', s.Last_Name) as driver_name
                          FROM DriverAssignment da 
                          JOIN Driver d ON da.StaffID = d.StaffID
                          JOIN Staff s ON d.StaffID = s.StaffID 
                          ORDER BY da.AssignmentID"""
            self.db.cursor.execute(query)
            for row in self.db.cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch assignment data: {str(e)}")

    def on_item_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            fields = ["AssignmentID", "BusID", "AssignmentDate", "EndDate"]
            for i, field in enumerate(fields):
                self.entries[field].delete(0, tk.END)
                if i < len(values) and values[i] is not None:
                    self.entries[field].insert(0, values[i])
            driver_name = values[5]
            for display_text, sid in self.driver_map.items():
                if driver_name in display_text:
                    self.driver_combo.set(display_text)
                    break

    def select_assignment(self):
        try:
            assignment_id = self.entries["AssignmentID"].get()
            if not assignment_id:
                messagebox.showwarning("Input Required", "Please enter an Assignment ID to select.")
                return

            query = """SELECT da.AssignmentID, da.BusID, da.AssignmentDate, 
                          da.EndDate, da.StaffID, CONCAT(s.First_Name, ' ', s.Last_Name)
                       FROM DriverAssignment da
                       JOIN Driver d ON da.StaffID = d.StaffID
                       JOIN Staff s ON d.StaffID = s.StaffID
                       WHERE da.AssignmentID = %s"""
            self.db.cursor.execute(query, (assignment_id,))
            result = self.db.cursor.fetchone()

            if result:
                fields = ["AssignmentID", "BusID", "AssignmentDate", "EndDate"]
                for i, field in enumerate(fields):
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, result[i])
                driver_name = result[5]
                for display_text in self.driver_map:
                    if driver_name in display_text:
                        self.driver_combo.set(display_text)
                        break

                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == int(assignment_id):
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break
            else:
                messagebox.showinfo("Not Found", "That Assignment ID does not exist")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to select assignment: {str(e)}")
