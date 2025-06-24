-- =====================================================
-- תוכנית ראשית 1: ניתוח ביצועי נהגים
-- Main Program 1: Driver Performance Analysis
-- =====================================================

-- ===== פונקציה 1: חישוב סכום משכורות נהג עם בונוסים =====
CREATE OR REPLACE FUNCTION calculate_driver_total_salary(
    p_staff_id INT,
    p_start_date DATE DEFAULT NULL,
    p_end_date DATE DEFAULT NULL
) RETURNS TABLE(
    staff_id INT,
    driver_name TEXT,
    total_salary NUMERIC,
    total_bonus NUMERIC,
    payment_count INT,
    avg_salary NUMERIC
) AS $$
DECLARE
    v_driver_record RECORD;
    v_salary_cursor CURSOR(driver_id INT, start_dt DATE, end_dt DATE) FOR
        SELECT s.amount, s.bonus, s.paymentdate 
        FROM salary s 
        WHERE s.staffid = driver_id 
        AND (start_dt IS NULL OR s.paymentdate >= start_dt)
        AND (end_dt IS NULL OR s.paymentdate <= end_dt);
    v_salary_rec RECORD;
    v_total_salary NUMERIC := 0;
    v_total_bonus NUMERIC := 0;
    v_count INT := 0;
    v_temp_bonus INT;
BEGIN
    -- Exception handling
    BEGIN
        -- בדיקה שהנהג קיים
        SELECT st.staffid, st.first_name || ' ' || st.last_name as full_name
        INTO v_driver_record
        FROM staff st
        JOIN driver d ON st.staffid = d.staffid
        WHERE st.staffid = p_staff_id;
        
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Driver with ID % not found', p_staff_id;
        END IF;
        
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE EXCEPTION 'Driver with ID % does not exist', p_staff_id;
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error finding driver: %', SQLERRM;
    END;
    
    -- פתיחת cursor וחישוב סכומים
    OPEN v_salary_cursor(p_staff_id, p_start_date, p_end_date);
    
    LOOP
        FETCH v_salary_cursor INTO v_salary_rec;
        EXIT WHEN NOT FOUND;
        
        v_total_salary := v_total_salary + v_salary_rec.amount;
        
        -- טיפול בבונוס (יכול להיות NULL)
        v_temp_bonus := COALESCE(v_salary_rec.bonus, 0);
        v_total_bonus := v_total_bonus + v_temp_bonus;
        
        v_count := v_count + 1;
    END LOOP;
    
    CLOSE v_salary_cursor;
    
    -- החזרת התוצאות
    RETURN QUERY SELECT 
        v_driver_record.staffid,
        v_driver_record.full_name,
        v_total_salary,
        v_total_bonus,
        v_count,
        CASE WHEN v_count > 0 THEN v_total_salary / v_count ELSE 0 END;
END;
$$ LANGUAGE plpgsql;

-- =====   Ref Cursor פונקציה 2: קבלת פרטי נהגים עם =====
CREATE OR REPLACE FUNCTION get_drivers_with_assignments()
RETURNS REFCURSOR AS $$
DECLARE
    drivers_cursor REFCURSOR := 'drivers_ref';
BEGIN
    OPEN drivers_cursor FOR
        SELECT 
            s.staffid,
            s.first_name,
            s.last_name,
            s.phone,
            s.email,
            dl.expirydate as license_expiry,
            da.busid,
            da.assignmentdate,
            da.enddate,
            CASE 
                WHEN da.enddate IS NULL THEN 'Active'
                WHEN da.enddate > CURRENT_DATE THEN 'Future'
                ELSE 'Completed'
            END as assignment_status
        FROM staff s
        JOIN driver d ON s.staffid = d.staffid
        LEFT JOIN driverlicense dl ON d.staffid = dl.staffid
        LEFT JOIN driverassignment da ON d.staffid = da.staffid
        ORDER BY s.staffid, da.assignmentdate DESC;
    
    RETURN drivers_cursor;
END;
$$ LANGUAGE plpgsql;

-- ===== פרוצדורה: ניהול הקצאות נהגים לאוטובוסים =====
CREATE OR REPLACE PROCEDURE manage_driver_assignments(
    p_staff_id INT,
    p_bus_id INT,
    p_assignment_date DATE DEFAULT CURRENT_DATE,
    p_action VARCHAR(10) DEFAULT 'ASSIGN' -- ASSIGN, END, EXTEND
)
LANGUAGE plpgsql AS $$
DECLARE
    v_driver_record RECORD;
    v_current_assignment RECORD;
    v_assignment_count INT;
    v_new_end_date DATE;
BEGIN
    -- בדיקת קיום הנהג
    SELECT s.staffid, s.first_name, s.last_name
    INTO v_driver_record
    FROM staff s
    JOIN driver d ON s.staffid = d.staffid
    WHERE s.staffid = p_staff_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Driver with ID % not found', p_staff_id;
    END IF;
    
    -- בדיקת הקצאה נוכחית
    SELECT * INTO v_current_assignment
    FROM driverassignment 
    WHERE staffid = p_staff_id AND (enddate IS NULL OR enddate > CURRENT_DATE)
    ORDER BY assignmentdate DESC
    LIMIT 1;
    
    CASE p_action
        WHEN 'ASSIGN' THEN
            -- בדיקה שאין הקצאה פעילה
            IF v_current_assignment.assignmentid IS NOT NULL THEN
                RAISE EXCEPTION 'Driver % already has an active assignment', p_staff_id;
            END IF;
            
            -- הקצאה חדשה
            INSERT INTO driverassignment (busid, assignmentdate, staffid)
            VALUES (p_bus_id, p_assignment_date, p_staff_id);
            
            RAISE NOTICE 'Assigned driver % to bus %', p_staff_id, p_bus_id;
            
        WHEN 'END' THEN
            IF v_current_assignment.assignmentid IS NULL THEN
                RAISE EXCEPTION 'No active assignment found for driver %', p_staff_id;
            END IF;
            
            -- סיום הקצאה
            UPDATE driverassignment 
            SET enddate = p_assignment_date
            WHERE assignmentid = v_current_assignment.assignmentid;
            
            RAISE NOTICE 'Ended assignment for driver %', p_staff_id;
            
        WHEN 'EXTEND' THEN
            IF v_current_assignment.assignmentid IS NULL THEN
                RAISE EXCEPTION 'No active assignment found for driver %', p_staff_id;
            END IF;
            
            -- הארכת הקצאה (30 יום)
            v_new_end_date := COALESCE(v_current_assignment.enddate, CURRENT_DATE) + INTERVAL '30 days';
            
            UPDATE driverassignment 
            SET enddate = v_new_end_date
            WHERE assignmentid = v_current_assignment.assignmentid;
            
            RAISE NOTICE 'Extended assignment for driver % until %', p_staff_id, v_new_end_date;
            
        ELSE
            RAISE EXCEPTION 'Invalid action: %. Use ASSIGN, END, or EXTEND', p_action;
    END CASE;
    
    -- ספירת סך כל ההקצאות
    SELECT COUNT(*) INTO v_assignment_count
    FROM driverassignment 
    WHERE staffid = p_staff_id;
    
    RAISE NOTICE 'Driver % now has % total assignments', p_staff_id, v_assignment_count;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in manage_driver_assignments: %', SQLERRM;
END;
$$;


-- ===== תוכנית ראשית 1: ניתוח ביצועי נהגים =====
CREATE OR REPLACE PROCEDURE main_driver_performance_analysis(
    p_month INT DEFAULT EXTRACT(MONTH FROM CURRENT_DATE),
    p_year INT DEFAULT EXTRACT(YEAR FROM CURRENT_DATE)
)
LANGUAGE plpgsql AS $$
DECLARE
    v_driver_cursor REFCURSOR;
    v_driver_rec RECORD;
    v_salary_info RECORD;
    v_start_date DATE;
    v_end_date DATE;
    v_total_drivers INT := 0;
    v_active_drivers INT := 0;
BEGIN
    RAISE NOTICE '=== Driver Performance Analysis for %/% ===', p_month, p_year;
    
    -- הגדרת טווח תאריכים
    v_start_date := DATE(p_year || '-' || p_month || '-01');
    v_end_date := v_start_date + INTERVAL '1 month' - INTERVAL '1 day';
    
    -- קריאה לפונקציה המחזירה ref cursor
    SELECT get_drivers_with_assignments() INTO v_driver_cursor;
    
    LOOP
        FETCH v_driver_cursor INTO v_driver_rec;
        EXIT WHEN NOT FOUND;
        
        v_total_drivers := v_total_drivers + 1;
        
        -- בדיקה אם הנהג פעיל
        IF v_driver_rec.assignment_status = 'Active' THEN
            v_active_drivers := v_active_drivers + 1;
            
            -- קריאה לפונקציה לחישוב משכורת
            SELECT * INTO v_salary_info
            FROM calculate_driver_total_salary(
                v_driver_rec.staffid, 
                v_start_date, 
                v_end_date
            );
            
            RAISE NOTICE 'Driver: % % (ID: %) - Total Salary: %, Payments: %',
                        v_driver_rec.first_name,
                        v_driver_rec.last_name,
                        v_driver_rec.staffid,
                        v_salary_info.total_salary,
                        v_salary_info.payment_count;
                        
            -- הארכת הקצאה לנהגים עם ביצועים טובים
            IF v_salary_info.payment_count > 15 AND v_salary_info.total_salary > 50000 THEN
                CALL manage_driver_assignments(
                    v_driver_rec.staffid,
                    v_driver_rec.busid,
                    CURRENT_DATE,
                    'EXTEND'
                );
            END IF;
        END IF;
    END LOOP;
    
    CLOSE v_driver_cursor;
    
    RAISE NOTICE 'Analysis Complete: % total drivers, % active drivers', 
                 v_total_drivers, v_active_drivers;
END;
$$;

