--Add staff
INSERT INTO Staff (StaffID, First_Name, Last_Name, Phone, Email, Hire_Date) 
VALUES 
(401, 'John', 'Doe', '123456789', 'john@example.com', '2022-05-10'),
(402, 'Alice', 'Smith', '987654321', 'alice@example.com', '2020-08-15'),
(403, 'Bob', 'Johnson', '555666777', 'bob@example.com', '2021-02-20');

-- Add Attendance
INSERT INTO Attendance (currentDate, Status, StaffID) 
VALUES 
('2024-03-01', 'Present', 401),
('2024-03-02', 'Late', 402),
('2024-03-03', 'Absent', 403);

-- Add Salary
INSERT INTO Salary (Amount, PaymentDate, Bonus, StaffID) 
VALUES 
(5000, '2024-02-28', 500, 401),
(7000, '2024-02-28', 700, 402),
(4500, '2024-02-28', NULL, 403);

-- Add Driver
INSERT INTO Driver (StaffID) 
VALUES 
(401), (402), (403);

-- Add DriverLicense
INSERT INTO DriverLicense (ExpiryDate, IssuedDate, StaffID) 
VALUES 
('2026-12-31', '2023-01-15', 401),
('2027-08-20', '2023-05-10', 402),
('2025-06-10', '2022-09-05', 403);

-- Add to Schedule
INSERT INTO Schedule (ShiftStart, ShiftEnd, StaffID) 
VALUES 
('2024-03-24 08:00:00', '2024-03-24 16:00:00', 401),
('2024-03-24 10:00:00', '2024-03-24 18:00:00', 402),
('2024-03-24 12:00:00', '2024-03-24 20:00:00', 403);

-- Add DriverAssignment
INSERT INTO DriverAssignment (BusID, AssignmentDate, EndDate, StaffID) 
VALUES 
(101, '2024-03-01', '2024-03-10', 401),
(102, '2024-03-05', NULL, 402),
(103, '2024-03-10', '2024-03-20', 403);