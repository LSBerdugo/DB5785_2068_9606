import random
from datetime import datetime, timedelta

# List of 400 unique 9-digit StaffIDs
staff_ids = [i for i in range(1, 1000)]

# Possible attendance statuses
status_options = ["Present", "Absent", "Late"]

# Generate random attendance records
start_date = datetime(2023, 1, 1)  # Adjust as needed
end_date = datetime(2025, 1, 1)

# Open SQL file to write inserts
with open("Attendance_insert.sql", "w") as file:
    file.write("INSERT INTO Attendance (AttendanceID, currentDate, Status, StaffID) VALUES\n")

    values = []
    for i in range(400):
        attendance_id = i + 1  # SERIAL starts from 1
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        status = random.choice(status_options)
        staff_id = random.choice(staff_ids)
        values.append(f"({attendance_id}, '{random_date.date()}', '{status}', {staff_id})")

    file.write(",\n".join(values) + ";\n")

print("SQL insert statements written to Attendance_insert.sql")