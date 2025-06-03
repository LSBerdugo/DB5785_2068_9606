-- Create a view that combines bus and route information from foreign tables
CREATE VIEW BusRouteDetailsView AS
SELECT
  b.bus_id,                -- Unique identifier for the bus
  b.license_plate,         -- License plate number of the bus
  b.capacity,              -- Number of passengers the bus can carry
  r.route_number,          -- Identifier of the route assigned to the bus
  r.start_location,        -- Starting point of the route
  r.end_location,          -- Ending point of the route
  r.length_km,             -- Length of the route in kilometers
  r.active                 -- Whether the route is currently active (TRUE/FALSE)
FROM foreign_buses b
JOIN foreign_routes r ON b.route_number = r.route_number; -- Join on route_number to combine bus and route details

-- Query 1: Select all active routes that are longer than 5 km
-- This helps filter only currently used routes with a significant length
SELECT *
FROM BusRouteDetailsView
WHERE active = TRUE AND length_km > 5;


-- -- Query 2:Select detailed info about the longest active bus routes per start location
SELECT
  b.bus_id,            -- Unique bus identifier
  b.license_plate,     -- Bus license plate number
  b.route_number,      -- Route number assigned to the bus
  b.start_location,    -- Route starting point
  b.end_location,      -- Route ending point
  b.length_km,         -- Route length in kilometers
  b.capacity           -- Passenger capacity of the bus
FROM BusRouteDetailsView b
JOIN (
    -- Subquery: find the maximum route length for each start location among active routes
    SELECT
      start_location,      -- Route starting location
      MAX(length_km) AS max_length  -- Longest route length per start location
    FROM BusRouteDetailsView
    WHERE active = TRUE    -- Only consider active routes
    GROUP BY start_location
) sub ON b.start_location = sub.start_location
     AND b.length_km = sub.max_length  -- Match the longest route per start location
WHERE b.active = TRUE    -- Ensure selected routes are currently active
;



-- Create a view that displays which staff member (driver) is assigned to which bus
CREATE VIEW DriverBusAssignments AS
 SELECT 
 da.StaffID,                   -- Unique ID of the driver (staff member)
  s.first_name AS driver_first_name, -- Driver's first name
  s.last_name AS driver_last_name,   -- Driver's last name
  b.bus_id,                    -- Bus ID assigned to the driver
  b.license_plate,             -- License plate of the assigned bus
  da.AssignmentDate,           -- Date the driver started the assignment
  da.EndDate                   -- End date of the driver's assignment (can be NULL if ongoing)
 FROM DriverAssignment da
 JOIN foreign_buses b ON da.BusID = b.bus_id  -- Match assignment to the actual bus
 JOIN Staff s ON da.StaffID = s.StaffID; -- Match assignment to the staff (driver) details
 

-- Query 1: Select the bus assignments of a specific driver named "kuku washere"
-- Useful for tracking the assignment history of a specific driver
SELECT *
FROM DriverBusAssignments
WHERE driver_first_name = 'kuku' AND driver_last_name = 'washere'; 


-- Query 2: This query retrieves information about drivers who have completed bus assignments
--that lasted more than 10 days. It shows the driver's ID, name, the bus license plate,
--the start and end dates of the assignment, and calculates how many days the assignment lasted.
--The results are ordered by the longest assignment duration first.
SELECT
  StaffID,                 -- Unique identifier of the staff (driver)
  driver_first_name,       -- Driver's first name
  driver_last_name,        -- Driver's last name
  license_plate,           -- License plate of the assigned bus
  AssignmentDate,          -- Date the driver started the bus assignment
  EndDate,                 -- Date the assignment ended (not NULL means the assignment is finished)
  (EndDate - AssignmentDate) AS days_assigned  -- Number of days the driver was assigned to the bus
FROM DriverBusAssignments
WHERE EndDate IS NOT NULL                    -- Only consider completed assignments
  AND (EndDate - AssignmentDate) > 10       -- Filter assignments longer than 30 days
ORDER BY days_assigned DESC;                 -- Sort results by longest assignments first