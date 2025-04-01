import random
from datetime import datetime, timedelta

# List of StaffIDs
staff_ids = [i for i in range(1000)]

# Define start and end date
start_date = datetime(2024, 11, 1)
end_date = datetime(2025, 1, 1)

# Open SQL file to write inserts
with open("Schedule_insert.sql", "w") as file:
    file.write("INSERT INTO Schedule (ScheduleID, ShiftStart, ShiftEnd, StaffID) VALUES\n")

    values = []
    for i in range(400):
        schedule_id = i + 1
        shift_start = start_date + timedelta(days=random.randint(0, (end_date - start_date).days),
                                             hours=random.randint(6, 18))
        shift_end = shift_start + timedelta(hours=random.randint(4, 10))  # 4-10 hour shifts
        staff_id = random.choice(staff_ids)

        values.append(f"({schedule_id}, '{shift_start.strftime('%Y-%m-%d %H:%M:%S')}', "
                      f"'{shift_end.strftime('%Y-%m-%d %H:%M:%S')}', {staff_id})")

    file.write(",\n".join(values) + ";\n")

print("SQL insert statements written to Schedule_insert.sql")
