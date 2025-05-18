

UPDATE Salary
SET Bonus = 1000
SELECT * FROM Salary
WHERE StaffID IN (
SELECT StaffID
FROM Attendance
WHERE EXTRACT (MONTH FROM currentDate) = EXTRACT (MONTH FROM (CURRENT_DATE - INTERVAL '1 month'))
AND EXTRACT (YEAR FROM currentDate) = EXTRACT(YEAR FROM (CURRENT_DATE - INTERVAL '1 month')
AND Status = 'Present'
GROUP BY StaffID
HAVING COUNT (*) = 15
)

UPDATE Schedule
SET ShiftEnd = ShiftStart + INTERVAL '8 hours'
WHERE ShiftEnd IS NULL
AND DATE(ShiftStart) < CURRENT_DATE;


UPDATE Salary
SET Amount = Amount - 100
WHERE StaffID IN(
SELECT StaffID
FROM Attendance
WHERE Status = 'Late'
AND currentDate >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY StaffID
HAVING COUNT (*) > 5
);
