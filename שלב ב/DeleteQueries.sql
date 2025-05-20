
DELETE FROM Staff
WHERE StaffID NOT IN(
SELECT StaffID
FROM Attendance
WHERE currentDate >= CURRENT_DATE - INTERVAL '30 days'
);



DELETE FROM Driver
WHERE StaffID IN (
SELECT dl.StaffID
FROM DriverLicense dl
WHERE dl.ExpiryDate < CURRENT_DATE
);


DELETE FROM DriverAssignment
WHERE (StaffID, AssignmentDate) IN (
SELECT da.StaffID, da.AssignmentDate
FROM DriverAssignment da
JOIN DriverLicense dl ON da.StaffID = dl.StaffID
WHERE da.AssignmentDate > CURRENT_DATE
AND da.AssignmentDate > dl.ExpiryDate
);
