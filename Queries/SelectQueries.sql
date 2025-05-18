

SELECT
s.First_Name,
s.Last_Name,
a.currentDate
FROM Attendance a
JOIN Staff s ON a. StaffID = s.StaffID
JOIN (
SELECT currentDate
FROM Attendance
WHERE Status = 'Absent'
GROUP BY currentDate
HAVING COUNT (*) = (
SELECT MAX (AbsentCount)
FROM (
SELECT COUNT (*) AS AbsentCount
FROM Attendance
WHERE Status = 'Absent'
GROUP BY currentDate
) AS sub
)
) AS max_absence_days ON a.currentDate = max_absence_days.currentDate
WHERE a. Status = 'Present'
ORDER BY a.currentDate, s.Last_Name;



SELECT to_char(sa. PaymentDate, 'Month') AS MonthName,
s.First_Name, s.Last_Name, sa.Bonus
FROM Salary sa
JOIN Staff s ON s. StaffID = sa. StaffID
WHERE sa. Bonus IS NOT NULL
AND EXTRACT (MONTH FROM sa. PaymentDate) = (
SELECT EXTRACT (MONTH FROM sa2. PaymentDate)
FROM Salary sa2
WHERE sa2. Bonus IS NOT NULL
GROUP BY EXTRACT (MONTH FROM sa2. PaymentDate)
ORDER BY SUM(sa2. Bonus) DESC
LIMIT 1
);

SELECT s.StaffID, s. First_Name, s.Last_Name, sa.Amount
FROM Staff s
JOIN Salary sa ON s. StaffID = sa. StaffID
WHERE EXTRACT (MONTH FROM sa. PaymentDate) = EXTRACT (MONTH FROM CURRENT_DATE)
AND sa. Amount > (
SELECT AVG(sa2.Amount)
FROM Salary sa2
WHERE EXTRACT (MONTH FROM sa2. PaymentDate) = EXTRACT (MONTH FROM CURRENT_DATE)
);

SELECT s.StaffID, s.First_Name, s.Last_Name
FROM Staff s
JOIN Attendance a ON s.StaffID = a.StaffID
JOIN Salary sal ON s.StaffID = sal. StaffID
WHERE a. Status = 'Present'
AND (sal. Bonus IS NULL OR sal. Bonus = 0)




SELECT s.StaffID, s. First_Name, s. Last_Name, dl. ExpiryDate, da.AssignmentDate
FROM DriverLicense dl
JOIN DriverAssignment da ON dl. StaffID = da. StaffID
JOIN Staff s ON s.StaffID = dl.StaffID
WHERE dl. ExpiryDate <= da. AssignmentDate + INTERVAL '90 days';

SELECT DISTINCT s.StaffID, s.First_Name, s.Last_Name, sch. ShiftStart
FROM Schedule sch
JOIN Staff s ON s. StaffID = sch. StaffID
JOIN Driver d ON d. StaffID = s. StaffID
WHERE EXTRACT (DOW FROM sch. ShiftStart) IN (0, 6);

SELECT s.StaffID, s. First_Name, s.Last_Name, sal.Amount
FROM Staff s
JOIN Salary sal ON s.StaffID = sal. StaffID
LEFT JOIN Schedule sch ON s. StaffID = sch. StaffID
WHERE sch.StaffID IS NULL 
AND sal. Amount > 0
ORDER BY sal.Amount DESC;


SELECT s.StaffID, s. First_Name, s.Last_Name,
sch.ShiftStart, sch.ShiftEnd,
sch. ShiftEnd - sch.ShiftStart AS Duration
FROM Schedule sch
JOIN Staff s ON s. StaffID = sch. StaffID
WHERE EXTRACT (YEAR FROM sch. ShiftStart) = EXTRACT (YEAR FROM CURRENT_DATE)
ORDER BY Duration DESC

