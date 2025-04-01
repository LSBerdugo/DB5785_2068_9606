CREATE TYPE status_enum AS ENUM('Present' , 'Absent' , 'Late');



CREATE TABLE Staff
(
  StaffID INT NOT NULL,
  First_Name VARCHAR(20) NOT NULL,
  Last_Name VARCHAR(20)  NOT NULL,
  Phone VARCHAR(20)  NOT NULL,
  Email VARCHAR(30)  NOT NULL,
  Hire_Date DATE NOT NULL,
  PRIMARY KEY (StaffID)
);

CREATE TABLE Attendance
(
  AttendanceID SERIAL PRIMARY KEY,
  currentDate DATE NOT NULL,
  Status status_enum NOT NULL,
  StaffID INT NOT NULL,
  FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

CREATE TABLE Salary
(
  SalaryID SERIAL PRIMARY KEY,
  Amount INT NOT NULL,
  PaymentDate DATE NOT NULL,
  Bonus INT,
  StaffID INT NOT NULL,
  FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

CREATE TABLE Driver
(
  StaffID INT NOT NULL,
  PRIMARY KEY (StaffID),
  FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

CREATE TABLE Schedule
(
  ScheduleID SERIAL PRIMARY KEY,
  ShiftStart TIMESTAMP NOT NULL,
  ShiftEnd TIMESTAMP NOT NULL,
  StaffID INT NOT NULL,
  FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

CREATE TABLE DriverLicense
(
  LicenseID SERIAL PRIMARY KEY,
  ExpiryDate DATE NOT NULL,
  IssuedDate DATE NOT NULL,
  StaffID INT NOT NULL,
  FOREIGN KEY (StaffID) REFERENCES Driver(StaffID) ON DELETE CASCADE
);

CREATE TABLE DriverAssignment
(
  AssignmentID SERIAL PRIMARY KEY,
  BusID INT NOT NULL,
  AssignmentDate DATE NOT NULL,
  EndDate DATE,
  StaffID INT NOT NULL,
  FOREIGN KEY (StaffID) REFERENCES Driver(StaffID) ON DELETE CASCADE
);