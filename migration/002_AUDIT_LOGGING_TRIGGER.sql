CREATE OR REPLACE FUNCTION log_audit()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO AuditLogs (action, timestamp)
    VALUES (TG_OP || ' in ' || TG_TABLE_NAME, NOW()); -- blya don't forgive SET current_user
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER employee_audit
AFTER INSERT OR UPDATE OR DELETE ON Employees
FOR EACH ROW EXECUTE FUNCTION log_audit();

CREATE TRIGGER project_audit
AFTER INSERT OR UPDATE OR DELETE ON Projects
FOR EACH ROW EXECUTE FUNCTION log_audit();
