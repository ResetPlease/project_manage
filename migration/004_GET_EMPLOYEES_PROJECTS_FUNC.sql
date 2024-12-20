CREATE OR REPLACE FUNCTION get_employee_projects(emp_id INTEGER)
RETURNS TABLE(project_id INTEGER, project_name TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name
    FROM Projects p
    JOIN Assignments a ON p.id = a.project_id
    WHERE a.employee_id = emp_id;
END;
$$ LANGUAGE plpgsql;
