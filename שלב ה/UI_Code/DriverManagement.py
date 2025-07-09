import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import psycopg2

class DriverManagement:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Driver Management")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f8f0fc')

        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        title_font = Font(family="Segoe UI", size=22, weight="bold")
        label_font = ('Segoe UI', 11)
        button_font = ('Segoe UI', 10, 'bold')

        # Title
        title = tk.Label(self.window, text="🚌 Driver Management", font=title_font, bg='#f8f0fc', fg='#4b3f72')
        title.pack(pady=20)

        # Form Section
        form_frame = tk.LabelFrame(self.window, text="Driver Information",
                                   font=('Segoe UI', 13, 'bold'), bg='#f8f0fc', fg='#4b3f72', bd=2, relief='groove')
        form_frame.pack(pady=10, padx=30, fill='x')

        # Staff ID Input
        tk.Label(form_frame, text="Staff ID:", font=label_font, bg='#f8f0fc').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.staff_id_entry = tk.Entry(form_frame, font=label_font, width=25)
        self.staff_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Button Area
        btn_frame = tk.Frame(form_frame, bg='#f8f0fc')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=15)

        button_configs = [
            ("➕ Add Driver", self.add_driver, '#a2d2ff'),
            ("❌ Remove", self.remove_driver, '#ffc9de'),
            ("🧹 Clear", self.clear_form, '#b5ead7')
        ]

        for text, command, color in button_configs:
            tk.Button(btn_frame, text=text, command=command,
                      bg=color, fg='black', font=button_font,
                      width=14, height=1, bd=0, relief='ridge',
                      activebackground=color, cursor='hand2').pack(side='left', padx=10)


        # Treeview Section
        list_frame = tk.LabelFrame(self.window, text="Driver List",
                                   font=('Segoe UI', 13, 'bold'), bg='#f8f0fc', fg='#4b3f72')
        list_frame.pack(pady=10, padx=30, fill='both', expand=True)

        self.tree = ttk.Treeview(list_frame, columns=("StaffID", "First Name", "Last Name"),
                                 show='headings', height=12)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), background="#e6e6fa", foreground="#4b3f72")
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=30, background="white", fieldbackground="white")

        for col in ("StaffID", "First Name", "Last Name"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=250)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.db.cursor.execute("""
            SELECT d.StaffID, s.First_Name, s.Last_Name 
            FROM Driver d
            JOIN Staff s ON d.StaffID = s.StaffID
        """)
        for row in self.db.cursor.fetchall():
            self.tree.insert('', 'end', values=row)

    def add_driver(self):
        staff_id = self.staff_id_entry.get()
        if not staff_id:
            messagebox.showwarning("Missing Input", "Please enter Staff ID.")
            return

        try:
            self.db.cursor.execute("SELECT * FROM staff WHERE StaffID = %s", (staff_id,))
            if not self.db.cursor.fetchone():
                messagebox.showerror("Error", "No staff found with this ID.")
                return

            self.db.cursor.execute("INSERT INTO Driver (StaffID) VALUES (%s)", (staff_id,))
            self.db.connection.commit()
            messagebox.showinfo("Success", "Staff added as driver!")
            self.refresh_list()
            self.clear_form()
        except psycopg2.errors.UniqueViolation:
            self.db.connection.rollback()
            messagebox.showwarning("Exists", "This staff is already a driver")
        except Exception as e:
            self.db.connection.rollback()
            messagebox.showerror("Error", f"Something went wrong: {e}")

    def remove_driver(self):
        staff_id = self.staff_id_entry.get()
        if not staff_id:
            messagebox.showwarning("Missing Input", "Please enter Staff ID.")
            return

        try:
            self.db.cursor.execute("DELETE FROM Driver WHERE StaffID = %s", (staff_id,))
            if self.db.cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "No driver with that Staff ID.")
            else:
                self.db.connection.commit()
                messagebox.showinfo("Success", "Driver removed.")
                self.refresh_list()
                self.clear_form()
        except Exception as e:
            self.db.connection.rollback()
            messagebox.showerror("Error", f"Something went wrong: {e}")

    def clear_form(self):
        self.staff_id_entry.delete(0, tk.END)

