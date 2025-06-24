
-- =====================================================
-- טריגר 1: בדיקת תוקף רישיון נהיגה לפני הקצאה
-- Trigger 1: Check driver's license validity before assignment
-- =====================================================
CREATE OR REPLACE FUNCTION trigger_check_license_validity()
RETURNS TRIGGER AS $$
DECLARE
    v_license_expiry DATE;
    v_driver_name TEXT;
BEGIN
    -- קבלת פרטי רישיון הנהיגה
    SELECT dl.expirydate, s.first_name || ' ' || s.last_name
    INTO v_license_expiry, v_driver_name
    FROM driverlicense dl
    JOIN staff s ON dl.staffid = s.staffid
    WHERE dl.staffid = NEW.staffid;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No valid license found for driver with Staff ID %', NEW.staffid;
    END IF;
    
    -- בדיקת תוקף הרישיון
    IF v_license_expiry <= CURRENT_DATE THEN
        RAISE EXCEPTION 'License expired for driver % (%). Expiry date: %', 
                       v_driver_name, NEW.staffid, v_license_expiry;
    END IF;
    
    -- אזהרה אם הרישיון יפוג בתוך 30 יום
    IF v_license_expiry <= CURRENT_DATE + INTERVAL '30 days' THEN
        RAISE WARNING 'License for driver % (%) will expire soon on %', 
                     v_driver_name, NEW.staffid, v_license_expiry;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_license_before_assignment
    BEFORE INSERT OR UPDATE ON driverassignment
    FOR EACH ROW
    EXECUTE FUNCTION trigger_check_license_validity();


-- =====================================================
-- טריגר 2: מניעת כפילויות ברישומי נוכחות
-- Trigger 2: Prevent duplicate attendance records
-- =====================================================
CREATE OR REPLACE FUNCTION prevent_duplicate_attendance()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Attendance 
        WHERE StaffID = NEW.StaffID AND currentDate = NEW.currentDate
    ) THEN
        RAISE EXCEPTION 'Attendance already exists for staff ID % on date %', 
                        NEW.StaffID, NEW.currentDate;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_duplicate_attendance
BEFORE INSERT ON Attendance
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_attendance();