CREATE OR REPLACE PROCEDURE assign_employee_to_project(emp_id INTEGER, proj_id INTEGER, start_date DATE)
AS $$
BEGIN
    INSERT INTO Assignments (employee_id, project_id, start_date)
    VALUES (emp_id, proj_id, start_date);
END;
$$ LANGUAGE plpgsql;
