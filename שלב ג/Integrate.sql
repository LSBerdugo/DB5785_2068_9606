
-- Enable the postgres_fdw extension to support foreign data wrappers for PostgreSQL
CREATE EXTENSION postgres_fdw;

-- Create a Foreign Data Wrapper named 'my_fdw' with handler and validator functions
CREATE FOREIGN DATA WRAPPER my_fdw
HANDLER postgres_fdw_handler
VALIDATOR postgres_fdw_validator;

-- Define the foreign server connection details to the remote PostgreSQL database
SERVER foreign_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', -- Hostname of the foreign server
 dbname 'fpostgres' , -- Database name on the foreign server
  port '5432' -- Port number for connection
  )

-- Create a user mapping for the current user to authenticate on the foreign server
CREATE USER MAPPING FOR current_user
SERVER	foreign_server
OPTIONS (user 'postgres' , -- Username for the foreign server
 password 'dbdocker12' -- Password for the foreign user
 )


-- Create a local table 'routes' in the current database to store route data
CREATE TABLE routes (
    route_number INT PRIMARY KEY, -- Unique identifier for the route
    length_km DECIMAL(5,2),              -- Route length in kilometers with two decimals
    duration_minutes INT,                -- Duration of the route in minutes
    start_location VARCHAR(100), -- Starting location name
    end_location VARCHAR(100), -- Ending location name
    active BOOLEAN DEFAULT TRUE -- Indicates if the route is currently active
);


-- Create a local table 'buses' in the current database to store bus data
CREATE TABLE buses (
    bus_id INT PRIMARY KEY, -- Unique identifier for the bus
    route_number INT,            -- Foreign key referencing the route number       
    license_plate VARCHAR(30) UNIQUE NOT NULL, -- Unique bus license plate number
    line_num INT,  -- Bus line number
    capacity INT CHECK (capacity > 0), -- Capacity of the bus, must be positive
    FOREIGN KEY (route_number) REFERENCES routes(route_number) 
);

-- Create a foreign table 'foreign_routes' that maps to the 'routes' table on the foreign server
CREATE FOREIGN TABLE foreign_routes (
    route_number INT  ,  -- Route number column from the foreign table
    length_km DECIMAL(5,2),         -- Length in km from the foreign table   
    duration_minutes INT,           -- Duration in minutes from the foreign table    
    start_location VARCHAR(100), -- Starting location from the foreign table
    end_location VARCHAR(100),  -- Ending location from the foreign table
    active BOOLEAN DEFAULT TRUE -- Active status from the foreign table
)

SERVER foreign_server -- Specifies the foreign server to connect to
OPTIONS (schema_name 'public' ,  -- Schema name where the foreign table resides
 table_name 'routes'  -- Foreign table name in the remote database
 );



-- Create a foreign table 'foreign_buses' that maps to the 'buses' table on the foreign server
CREATE FOREIGN TABLE foreign_buses (
    bus_id INT , -- Bus ID from the foreign table
    route_number INT,                -- Route number from the foreign table   
    license_plate VARCHAR(30) ,  -- License plate from the foreign table
    line_num INT,  -- Line number from the foreign table
    capacity INT CHECK (capacity > 0)  -- Capacity with a constraint that it must be positive
   
)

SERVER foreign_server -- Specifies the foreign server to connect to
OPTIONS (schema_name 'public' , -- Schema name where the foreign table resides
 table_name 'buses' -- Foreign table name in the remote database
 );
 
