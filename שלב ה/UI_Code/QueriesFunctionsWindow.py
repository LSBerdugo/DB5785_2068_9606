import tkinter as tk
from tkinter import ttk, messagebox

ATTENDID = 1000

class QueriesFunctionsWindow:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Queries & Procedures")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f8f0fc')  # light pastel background
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#f8f0fc", borderwidth=0)
        style.configure("TNotebook.Tab", background="#f8f0fc")


# Combobox and Treeview pastel love
        style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff", foreground="#4b3f72")
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#4b3f72")
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), foreground="#4b3f72", background="#cdb4db")

        title = tk.Label(self.window, text="Reports & Tools", font=('Arial', 20, 'bold'),
                     bg='#f8f0fc', fg='#4b3f72')
        title.pack(pady=10)

        tabs = ttk.Notebook(self.window)
        tabs.pack(fill='both', expand=True)

        query_tab = tk.Frame(tabs, bg='#f8f0fc')
        func_tab = tk.Frame(tabs, bg='#f8f0fc')

        tabs.add(query_tab, text="Predefined Queries")
        tabs.add(func_tab, text="Functions & Procedures")

        self.setup_queries(query_tab)
        self.setup_functions(func_tab)


    def setup_queries(self, parent):
        queries = {
            "Staff Present on Most Absent Day": '''
                SELECT s.First_Name, s.Last_Name, a.currentDate
                FROM Attendance a
                JOIN Staff s ON a.StaffID = s.StaffID
                JOIN (
                    SELECT currentDate
                    FROM Attendance
                    WHERE Status = 'Absent'
                    GROUP BY currentDate
                    HAVING COUNT(*) = (
                        SELECT MAX(AbsentCount)
                        FROM (
                            SELECT COUNT(*) AS AbsentCount
                            FROM Attendance
                            WHERE Status = 'Absent'
                            GROUP BY currentDate
                        ) AS sub
                    )
                ) AS max_absence_days ON a.currentDate = max_absence_days.currentDate
                WHERE a.Status = 'Present'
                ORDER BY a.currentDate, s.Last_Name;
            ''',

            "Paid but No Schedule": '''
                SELECT s.StaffID, s.First_Name, s.Last_Name, sal.Amount
                FROM Staff s
                JOIN Salary sal ON s.StaffID = sal.StaffID
                LEFT JOIN Schedule sch ON s.StaffID = sch.StaffID
                WHERE sch.StaffID IS NULL AND sal.Amount > 0
                ORDER BY sal.Amount DESC;
            ''',

            "Drivers Working on Weekends": '''
                SELECT DISTINCT s.StaffID, s.First_Name, s.Last_Name, sch.ShiftStart
                FROM Schedule sch
                JOIN Staff s ON s.StaffID = sch.StaffID
                JOIN Driver d ON d.StaffID = s.StaffID
                WHERE EXTRACT(DOW FROM sch.ShiftStart) IN (0, 6);
            '''
        }

        self.query_var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=self.query_var, values=list(queries.keys()), state='readonly')
        combo.pack(pady=10)

        run_btn = tk.Button(parent, text="Run Query", command=lambda: self.run_query(queries),
                        bg='#a2d2ff', fg='black', font=('Arial', 10, 'bold'),
                        activebackground='#8bb9ff', relief='flat', bd=0, cursor='hand2')
        run_btn.pack(pady=5)


        self.query_results = ttk.Treeview(parent, show='headings')
        self.query_results.pack(fill='both', expand=True, padx=10, pady=10)


    def run_query(self, query_dict):
        selection = self.query_var.get()
        if not selection:
            messagebox.showwarning("Select Query", "Please select a query to run.")
            return

        query = query_dict[selection]
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            cols = [desc[0] for desc in self.db.cursor.description]

            self.query_results.delete(*self.query_results.get_children())
            self.query_results['columns'] = cols
            for col in cols:
                self.query_results.heading(col, text=col)
                self.query_results.column(col, width=100)

            for row in results:
                self.query_results.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

    def setup_functions(self, parent):
        label = tk.Label(parent, text="Choose Function/Procedure to Run:", font=('Arial', 12))
        label.pack(pady=5)

        # **Change 1: Adding input field to select Staff ID**
        # Create frame for input fields
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=10)

        # Field to select Staff ID
        tk.Label(input_frame, text="Staff ID:", font=('Arial', 10)).pack(side='left', padx=5)
        self.staff_id_entry = tk.Entry(input_frame, width=10)
        self.staff_id_entry.pack(side='left', padx=5)
        self.staff_id_entry.insert(0, "1")  # Default value

        tk.Button(parent, text="Get Attendance %",
                  command=lambda: self.get_attendance_dynamic(),
                  bg='#b5ead7', fg='black', font=('Arial', 10, 'bold'),
                  activebackground='#a0d9c4', relief='flat', bd=0).pack(pady=5)

        tk.Button(parent, text="Add Attendance Once",
              command=lambda: self.add_attendance_dynamic(),
              bg='#fdffb6', fg='black', font=('Arial', 10, 'bold'),
              activebackground='#fdf197', relief='flat', bd=0).pack(pady=5)

        tk.Button(parent, text="Get Drivers with Assignments",
              command=lambda: self.get_drivers_with_assignments(),
              bg='#cdb4db', fg='black', font=('Arial', 10, 'bold'),
              activebackground='#bca0cb', relief='flat', bd=0).pack(pady=5)


        self.func_output = tk.Text(parent, height=10, font=('Courier', 10))
        self.func_output.pack(fill='both', expand=True, padx=10, pady=10)

    # Function to get attendance percentage with validation
    def get_attendance_dynamic(self):
        try:
            # Read value from field and convert to number
            staff_id = int(self.staff_id_entry.get())
            # Build query with dynamic value
            query = f"SELECT get_attendance_percentage({staff_id})"
            # Call your existing function
            self.run_scalar_function(query, True)
        except ValueError:
            # Show error message if value is invalid
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, "Error: Please enter a valid Staff ID (number)\n")

    # Function to add attendance with validation
    def add_attendance_dynamic(self):
        """Function to add attendance with dynamic Staff ID"""
        try:
            # Read value from field and convert to number
            staff_id = int(self.staff_id_entry.get())
            global ATTENDID
            # Build query with dynamic value
            query = f"CALL add_attendance_once({ATTENDID}, {staff_id}, CURRENT_DATE, 'Present')"
            ATTENDID +=1
            # Call your existing function
            self.run_proc(query)
        except ValueError:
            # Show error message if value is invalid
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, "Error: Please enter a valid Staff ID (number)\n")

    def run_scalar_function(self, sql, show_result):
        try:
            self.db.cursor.execute(sql)
            result = self.db.cursor.fetchone()
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, f"Result: {result[0]}")
        except Exception as e:
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, f"Error: {str(e)}")

    def run_proc(self, sql):
        try:
            self.db.cursor.execute(sql)
            self.db.connection.commit()
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, "Procedure executed successfully.")
        except Exception as e:
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, f"Error: {str(e)}")

    def get_drivers_with_assignments(self):
        try:
            self.db.cursor.callproc("get_drivers_with_assignments")
            self.db.cursor.execute("FETCH ALL IN drivers_ref")
            results = self.db.cursor.fetchall()
            cols = [desc[0] for desc in self.db.cursor.description]

            self.func_output.delete(1.0, tk.END)
            # Show column headers
            self.func_output.insert(tk.END, '\t\t'.join(cols) + '\n')
            self.func_output.insert(tk.END, '-' * 100 + '\n')

            # Dump row data
            for row in results:
                self.func_output.insert(tk.END, '\t\t'.join(str(cell) if cell is not None else 'NULL' for cell in row) + '\n')

        except Exception as e:
            self.func_output.delete(1.0, tk.END)
            self.func_output.insert(tk.END, f"Error: {str(e)}")
