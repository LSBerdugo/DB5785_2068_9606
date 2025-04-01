import random
from datetime import datetime, timedelta

# List of StaffIDs
staff_ids = [i for i in range(1000)]

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 1, 1)

# Open SQL file to write inserts
with open("Salary_insert.sql", "w") as file:
    file.write("INSERT INTO Salary (SalaryID, Amount, PaymentDate, Bonus, StaffID) VALUES\n")

    values = []
    for i in range(400):
        salary_id = i + 1
        amount = random.randint(2000, 10000)
        payment_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        bonus = random.choice([None, random.randint(100, 2000)])
        staff_id = random.choice(staff_ids)

        if bonus:
            values.append(f"({salary_id}, {amount}, '{payment_date.strftime('%Y-%m-%d')}', {bonus}, {staff_id})")
        else:
            values.append(f"({salary_id}, {amount}, '{payment_date.strftime('%Y-%m-%d')}', NULL, {staff_id})")

    file.write(",\n".join(values) + ";\n")

print("SQL insert statements written to Salary_insert.sql")