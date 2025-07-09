import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class StaffManagement:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Staff Management")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f8f0fc')  # same pastel background
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        title_font = Font(family="Segoe UI", size=22, weight="bold")
        label_font = ('Segoe UI', 11)
        btn_font = ('Segoe UI', 10, 'bold')

        # Title
        title = tk.Label(self.window, text="Staff Management", font=title_font, bg='#f8f0fc', fg='#4b3f72')
        title.pack(pady=10)

        # Form Frame
        form_frame = tk.LabelFrame(self.window, text="Staff Information",
                                   font=("Segoe UI", 12, "bold"), bg='#f8f0fc', fg='#4b3f72')
        form_frame.pack(padx=20, pady=5, fill='x')

        self.entries = {}
        fields = ["StaffID", "First_Name", "Last_Name", "Phone", "Email", "Hire_Date"]
        placeholders = ["StaffID", "First Name", "Last Name", "Phone", "Email", "Hire Date"]

        for i, (field, placeholder) in enumerate(zip(fields, placeholders)):
            row = i // 3
            col = (i % 3) * 2
            tk.Label(form_frame, text=f"{placeholder}:", bg='#f8f0fc', fg='#4b3f72', font=label_font) \
                .grid(row=row, column=col, sticky='e', padx=8, pady=5)
            entry = tk.Entry(form_frame, width=25, font=('Segoe UI', 10))
            entry.grid(row=row, column=col+1, padx=8, pady=5)
            self.entries[field] = entry

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg='#f8f0fc')
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

        def create_btn(text, command, bg_color, icon=None):
            txt = f"{icon} {text}" if icon else text
            return tk.Button(btn_frame, text=txt, command=command,
                             bg=bg_color, fg='black', font=btn_font,
                             width=12, height=1, bd=0, relief='flat',
                             activebackground=bg_color)

        create_btn("Add", self.add_staff, '#a2d2ff', '➕').pack(side='left', padx=10)
        create_btn("Update", self.update_staff, '#cdb4db', '📝').pack(side='left', padx=10)
        create_btn("Delete", self.delete_staff, '#ffc9de', '❌').pack(side='left', padx=10)
        create_btn("Clear", self.clear_form, '#b5ead7', '🧹').pack(side='left', padx=10)
        create_btn("Select", self.select_staff, '#fdffb6', '🔍').pack(side='left', padx=10)

        # List Frame
        list_frame = tk.LabelFrame(self.window, text="Staff List",
                                   font=('Segoe UI', 12, 'bold'), bg='#f8f0fc', fg='#4b3f72')
        list_frame.pack(padx=20, pady=10, fill='both', expand=True)

        columns = ("ID", "First Name", "Last Name", "Phone", "Email", "Hire Date")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#8e9aaf", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25,
                        background="white", fieldbackground="white")
        style.map('Treeview', background=[('selected', '#a2d2ff')],
                  foreground=[('selected', 'black')])

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor='center')

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

        self.tree.bind('<Double-1>', self.on_item_select)

    def get_form_data(self):
        return tuple(self.entries[field].get() for field in
                     ["StaffID", "First_Name", "Last_Name", "Phone", "Email", "Hire_Date"])

    def add_staff(self):
        try:
            data = self.get_form_data()
            query = """INSERT INTO Staff (StaffID, First_Name, Last_Name, Phone, Email, Hire_Date) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            self.db.cursor.execute(query, data)
            self.db.connection.commit()
            messagebox.showinfo("Success", "Staff added successfully!")
            self.clear_form()
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add staff: {str(e)}")

    def update_staff(self):
        try:
            data = self.get_form_data()
            query = """UPDATE Staff SET First_Name=%s, Last_Name=%s, Phone=%s, 
                       Email=%s, Hire_Date=%s WHERE StaffID=%s"""
            self.db.cursor.execute(query, data[1:] + (data[0],))
            self.db.connection.commit()
            messagebox.showinfo("Success", "Staff updated successfully!")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update staff: {str(e)}")

    def delete_staff(self):
        staff_id = self.entries["StaffID"].get()
        if not staff_id:
            messagebox.showwarning("Warning", "Please enter Staff ID to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this staff member?"):
            try:
                query = "DELETE FROM Staff WHERE StaffID=%s"
                self.db.cursor.execute(query, (staff_id,))
                self.db.connection.commit()
                messagebox.showinfo("Deleted", "Staff deleted successfully!")
                self.clear_form()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete staff: {str(e)}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            query = "SELECT * FROM Staff ORDER BY StaffID"
            self.db.cursor.execute(query)
            for row in self.db.cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch staff data: {str(e)}")

    def on_item_select(self, event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            for i, field in enumerate(["StaffID", "First_Name", "Last_Name", "Phone", "Email", "Hire_Date"]):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, values[i])

    def select_staff(self):
        staff_id = self.entries["StaffID"].get()
        if not staff_id:
            messagebox.showwarning("Input Required", "Please enter a Staff ID to select.")
            return

        try:
            query = "SELECT * FROM Staff WHERE StaffID = %s"
            self.db.cursor.execute(query, (staff_id,))
            result = self.db.cursor.fetchone()

            if result:
                for i, field in enumerate(["StaffID", "First_Name", "Last_Name", "Phone", "Email", "Hire_Date"]):
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, result[i])
                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == int(staff_id):
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break
            else:
                messagebox.showinfo("Not Found", "No staff member found with that ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to select staff: {str(e)}")
