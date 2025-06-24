-- =====================================================
-- תוכנית ראשית 2: ניהול נוכחות עובדים
-- Main Program 2: Employee Attendance Management
-- =====================================================

-- ===== פונקציה 1: חישוב אחוזי נוכחות לעובד =====
-- Function 1: Calculate attendance percentage for a staff member
CREATE OR REPLACE FUNCTION get_attendance_percentage(p_staff_id INT)
RETURNS NUMERIC AS $$
DECLARE
    total_days INT;
    present_days INT;
BEGIN
    -- סופרים את כלל הימים שבהם נרשמה נוכחות
    SELECT COUNT(*) INTO total_days 
    FROM Attendance 
    WHERE StaffID = p_staff_id;

    -- אם אין כלל נוכחויות – אחוזי נוכחות יהיו 0
    IF total_days = 0 THEN
        RETURN 0;
    END IF;

    -- סופרים את הימים שבהם העובד היה נוכח
    SELECT COUNT(*) INTO present_days 
    FROM Attendance 
    WHERE StaffID = p_staff_id AND Status = 'Present';

    -- מחזירים אחוז עיגול לשתי ספרות אחרי הנקודה
    RETURN ROUND((present_days * 100.0) / total_days, 2);
END;
$$ LANGUAGE plpgsql;

-- ===== פרוצדורה 1: הוספת נוכחות לעובד (ללא כפילויות) =====
-- Procedure 1: Add attendance for a staff member (if not already exists)
CREATE OR REPLACE PROCEDURE add_attendance_once(
    p_attendId INT,
    p_staff_id INT, 
    p_date DATE, 
    p_status status_enum
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- בדיקה אם קיימת כבר נוכחות באותו תאריך
    IF NOT EXISTS (
        SELECT 1 
        FROM Attendance 
        WHERE StaffID = p_staff_id AND currentDate = p_date
    ) THEN
        -- הכנסת נוכחות חדשה
        INSERT INTO Attendance(attendanceid ,currentDate, Status, StaffID)
        VALUES (p_attendId ,p_date, p_status, p_staff_id);
    END IF;
END;
$$;


-- ===== פרוצדורה ראשית: בדיקת נוכחות יומית =====
-- Main Procedure: Daily attendance check and update
CREATE OR REPLACE PROCEDURE main_attendance_check(p_attendId INT, p_staff_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    percent NUMERIC;
BEGIN
    -- הוספת נוכחות "נוכח" ליום הנוכחי (אם לא קיימת)
    CALL add_attendance_once(p_attendId,p_staff_id, CURRENT_DATE, 'Present');

    -- חישוב אחוזי נוכחות
    percent := get_attendance_percentage(p_staff_id);

    -- הדפסת תוצאה
    RAISE NOTICE 'אחוזי נוכחות של העובד: %', percent;
END;
$$;