BEGIN;

UPDATE salary s
SET bonus = 2000
FROM staff st
WHERE s.staffid = st.staffid
  AND st.hire_date <= (CURRENT_DATE - INTERVAL '1 year') ;
                    
ROLLBACK;


BEGIN;

UPDATE salary s
SET bonus = 2000
FROM staff st
WHERE s.staffid = st.staffid
  AND st.hire_date <= (CURRENT_DATE - INTERVAL '1 year') ;
                    
COMMIT;


