ALTER TABLE Salary
ADD CONSTRAINT chk_salary_amount_positive
CHECK (Amount > 0);


ALTER TABLE DriverLicense
ADD CONSTRAINT chk_license_dates
CHECK (ExpiryDate > IssuedDate);



ALTER TABLE Schedule
ADD CONSTRAINT chk_shift_time
CHECK (ShiftEnd > ShiftStart);



ALTER TABLE DriverAssignment
ADD CONSTRAINT chk_assignment_dates
CHECK (EndDate IS NULL OR EndDate > AssignmentDate);



ALTER TABLE Staff
ADD CONSTRAINT chk_hire_date
CHECK (Hire_Date <= CURRENT_DATE);

